from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import IdeaWithTranslatedFieldsForm
from .models import Idea, IdeaWithTranslatedFields


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
    template_name = 'ideas/ideas_list.html'


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

    if request.method == 'POST':
        form = IdeaWithTranslatedFieldsForm(
            data=request.POST,
            files=request.FILES,
            instance=idea
        )
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:ideas_detail', pk=idea.pk)

    else:
        form = IdeaWithTranslatedFieldsForm(instance=idea)
    template_name = 'ideas/idea_form.html'
    context = {
        'title': 'Create or Update Idea',
        'form': form,
        'idea': idea
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
