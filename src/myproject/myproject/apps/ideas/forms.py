from django import forms

from myproject.apps.ideas.models import IdeaWithTranslatedFields


class IdeaWithTranslatedFieldsForm(forms.ModelForm):
    class Meta:
        model = IdeaWithTranslatedFields
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # django-crispy-forms
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
                    'placeholder': f'Idea {str(field)}',
                    'class': 'form-control',
                }
            )
