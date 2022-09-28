from django import forms

from .app_settings import ARTICLE_THEME_CHOICES
from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):
    """
    We created a custom ModelForm and set the choices there
    instead of doing it in models.py. This was done to avoid
    the creation of new database migrations whenever
    the ARTICLE_THEME_CHOICES is changed.
    """
    theme = forms.ChoiceField(
        label=NewsArticle._meta.get_field('theme').verbose_name,
        choices=ARTICLE_THEME_CHOICES,
        required=not NewsArticle._meta.get_field('theme').blank
    )

    class Meta:
        fields = '__all__'
