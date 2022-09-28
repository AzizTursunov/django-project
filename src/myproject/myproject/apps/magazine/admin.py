from django.contrib import admin

from .forms import NewsArticle, NewsArticleForm
from .models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleForm
