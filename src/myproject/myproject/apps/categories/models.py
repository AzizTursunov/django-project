from django.db import models
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.model_field import MultilingualCharField


class Category(models.Model):
    title = MultilingualCharField(
        _('Title'),
        max_length=100
    )
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
