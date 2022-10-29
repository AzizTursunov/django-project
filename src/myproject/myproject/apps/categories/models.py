from django.db import models
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.model_field import TranslatedField


class Category(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=200
    )
    translated_title = TranslatedField('title')
    slug = models.SlugField()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    # to access a model from another app in method, import model inside method
    def get_ideas_without_this_category(self):
        from myproject.apps.ideas.models import Idea
        return Idea.objects.exclude(category=self)

    def __str__(self):
        return str(self.title)


class CategoryTranslations(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        related_name='translations'
    )
    language = models.CharField(
        _('Language'),
        max_length=7
    )
    title = models.CharField(
        _('Title'),
        max_length=200
    )

    class Meta:
        verbose_name = _('Category Translations')
        verbose_name_plural = _('Category Translations')
        ordering = ['language']
        unique_together = [['category', 'language']]

    def __str__(self):
        return self.title
