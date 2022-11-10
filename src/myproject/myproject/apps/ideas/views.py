from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import (
    IdeaFilterForm,
    IdeaTranslationsForm,
    IdeaWithTranslatedFieldsForm
)
from .models import (
    Idea,
    IdeaTranslations,
    IdeaWithTranslatedFields,
    RATING_CHOICES
)

PAGE_SIZE = getattr(settings, 'PAGE_SIZE', 24)


def idea_detail_view(request, idea_id=None):
    idea = get_object_or_404(Idea, id=idea_id)
    is_translated = False
    template_name = 'ideas/idea_detail.html'
    lang_code_list = [
        item[0]
        for item in settings.LANGUAGES
        if item[0] != settings.LANGUAGE_CODE
    ]
    context = {
        'title': 'Idea detail',
        'object': idea,
        'is_translated': is_translated,
        'languages': lang_code_list
    }
    return render(request, template_name, context)


def idea_vs_translated_fields_view(request, idea_id=None):
    idea = get_object_or_404(IdeaWithTranslatedFields, id=idea_id)
    template_name = 'ideas/idea_detail.html'
    is_translated = True
    context = {
        'title': 'Idea detail',
        'object': idea,
        'is_translated': is_translated

    }
    return render(request, template_name, context)


class IdeaWithTranslatedFieldsListView(ListView):
    model = IdeaWithTranslatedFields
    template_name = 'ideas/idea_list.html'


class IdeaWithTranslatedFieldsDetailView(DetailView):
    model = IdeaWithTranslatedFields
    context_object_name = 'idea'
    template_name = 'ideas/idea_detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            IdeaWithTranslatedFieldsDetailView,
            self
        ).get_context_data(**kwargs)
        context['is_translated'] = True
        return context


@login_required
def create_or_update_idea_view(request, pk=None):
    idea = None
    if pk:
        idea = get_object_or_404(IdeaWithTranslatedFields, pk=pk)
    IdeaTranslationsFormSet = modelformset_factory(
        IdeaTranslations,
        form=IdeaTranslationsForm,
        extra=0, can_delete=True
    )

    if request.method == 'POST':
        form = IdeaWithTranslatedFieldsForm(
            request,
            data=request.POST,
            files=request.FILES,
            instance=idea
        )
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.filter(idea=idea),
            data=request.POST or None,
            files=request.FILES or None,
            prefix='translations',
            form_kwargs={'request': request}
        )
        if form.is_valid() and translations_formset.is_valid():
            idea = form.save()
            translations = translations_formset.save(
                commit=False
            )
            for translation in translations:
                translation.idea = idea
                translation.save()
            translations_formset.save_m2m()
            for translation in translations_formset.deleted_objects:
                translation.delete()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaWithTranslatedFieldsForm(request, instance=idea)
        translations_formset = IdeaTranslationsFormSet(
            queryset=IdeaTranslations.objects.filter(idea=idea),
            prefix='translations',
            form_kwargs={'request': request}
        )
    template_name = 'ideas/idea_form.html'
    context = {
        'title': 'Create or Update Idea',
        'form': form,
        'idea': idea,
        'translations_formset': translations_formset
    }

    return render(request, template_name, context)


@login_required
def delete_idea_view(request, pk):
    idea = get_object_or_404(IdeaWithTranslatedFields, pk=pk)
    if request.method == 'POST':
        idea.delete()
        return redirect('ideas:idea_list')
    context = {
        'title': 'Delete Idea',
        'idea':  idea
    }
    return render(
        request,
        'ideas/idea_deleting_confirmation.html',
        context
    )


def idea_with_translated_fields_list_view(request):
    qs = IdeaWithTranslatedFields.objects.order_by('title')
    form = IdeaFilterForm(data=request.GET)

    facets = {
        'selected': {},
        'categories': {
            'authors': form.fields['author'].queryset,
            'categories': form.fields['category'].queryset,
            'ratings': RATING_CHOICES
        }
    }

    if form.is_valid():
        filters = (
            ('author', 'author'),
            ('category', 'categories'),
            ('rating', 'rating')
        )
        qs = filter_facets(facets, qs, form, filters)

    context = {
        'form': form,
        'facets': facets,
        'object_list': qs
    }
    return render(request, 'ideas/idea_list.html', context)


def filter_facets(facets, qs, form, filters):
    for query_param, filter_param in filters:
        value = form.cleaned_data[query_param]
        if value:
            selected_value = value
            if query_param == 'rating':
                rating = int(value)
                selected_value = (rating, dict(RATING_CHOICES)[rating])
            facets['selected'][query_param] = selected_value
            filter_args = {filter_param: value}
            qs = qs.filter(**filter_args).distinct()
    return qs
