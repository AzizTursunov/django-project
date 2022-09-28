from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsArticle(models.Model):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255
    )
    body = models.TextField(
        verbose_name=_('Body')
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    theme = models.CharField(
        verbose_name=_('Theme'),
        max_length=20
    )
