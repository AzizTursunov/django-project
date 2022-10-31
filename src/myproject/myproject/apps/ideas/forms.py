from django import forms

from myproject.apps.ideas.models import IdeaWithTranslatedFields


class IdeaWithTranslatedFieldsForm(forms.ModelForm):
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

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.request.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
