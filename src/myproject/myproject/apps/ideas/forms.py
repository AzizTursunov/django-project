from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from crispy_forms import bootstrap, helper, layout

from myproject.apps.categories.models import Category
from .models import (
    IdeaTranslations,
    IdeaWithTranslatedFields,
    RATING_CHOICES
)

User = get_user_model()


class IdeaWithTranslatedFieldsForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = IdeaWithTranslatedFields
        exclude = ('author',)

    def __init__(self, request, *args, **kwargs):
        # django-crispy-forms
        self.request = request
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
                    'placeholder': f'Idea {str(field)}',
                    'class': 'form-control',
                }
            )
        title_field = layout.Field(
            'title',
            css_class='input-block-level'
        )
        content_field = layout.Field(
            'content',
            css_class='input-block-level',
            rows='3'
        )
        main_fieldset = layout.Fieldset(
            _('Main data'),
            title_field,
            content_field
        )
        picture_field = layout.Field(
            'picture',
            css_class='input-block-level'
        )
        format_html = layout.HTML(
            '''{% include "ideas/includes/picture_guidelines.html" %}'''
        )
        picture_fieldset = layout.Fieldset(
            _('Picture'),
            picture_field,
            format_html,
            title=_('Image upload'),
            csS_id='picture_fieldset'
        )
        categories_field = layout.Field(
            'categories',
            css_class='input-block-level'
        )
        categories_fieldset = layout.Fieldset(
            _('Categories'),
            categories_field,
            css_id='categories_fieldset'
        )
        inline_translations = layout.HTML(
            '''{% include "ideas/forms/translations.html" %}'''
        )
        submit_button = layout.Submit(
            'save',
            _('Save')
        )
        actions = bootstrap.FormActions(submit_button)
        self.helper = helper.FormHelper()
        self.helper.form_action = self.request.path
        self.helper.form_method = 'POST'
        self.helper.layout = layout.Layout(
            main_fieldset,
            inline_translations,
            picture_fieldset,
            categories_fieldset,
            actions
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class IdeaTranslationsForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_('Language'),
        choices=settings.LANGUAGES_EXCEPT_THE_DEFAULT,
        required=True,
    )

    class Meta:
        model = IdeaTranslations
        exclude = ['idea']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        id_field = layout.Field('id')
        language_field = layout.Field(
            'language',
            css_class='input_block-level'
        )
        title_field = layout.Field(
            'title',
            css_class='input_block-level'
        )
        content_field = layout.Field(
            'content',
            css_class='input_block-level',
            rows='3'
        )
        delete_field = layout.Field('DELETE')
        main_fieldset = layout.Fieldset(
            _('Main data'),
            id_field,
            language_field,
            title_field,
            content_field,
            delete_field
        )
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(main_fieldset)


class IdeaFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        label=_('Author'),
        required=False,
        queryset=User.objects.annotate(
            idea_count=models.Count('authored_ideas')
        ).filter(idea_count__gt=0)
    )
    category = forms.ModelChoiceField(
        label=_('Category'),
        required=False,
        queryset=Category.objects.annotate(
            idea_count=models.Count('category_ideas')
        ).filter(idea_count__gt=0)
    )
    rating = forms.ChoiceField(
        label=_('Rating'),
        required=False,
        choices=RATING_CHOICES
    )
