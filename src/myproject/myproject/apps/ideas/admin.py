from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from myproject.apps.core.admin import (
    LanguageChoiceForm,
    get_multilingual_field_names
)
from myproject.apps.ideas.models import (
    Comment,
    Idea,
    IdeaTranslations,
    IdeaWithTranslatedFields,
    Like
)

admin.site.register(Like)
admin.site.register(Comment)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            _('Title and Content'),
            {
                'fields': (
                    get_multilingual_field_names('title') +
                    get_multilingual_field_names('content')
                )
            }
        ),
        (
            _('Author and Category'),
            {'fields': ['author', 'category']}
        )
    ]


class IdeaTranslationsForm(LanguageChoiceForm):
    class Meta:
        model = IdeaTranslations
        fields = '__all__'


class IdeaTranslationsInline(admin.StackedInline):
    form = IdeaTranslationsForm
    model = IdeaTranslations
    extra = 0


@admin.register(IdeaWithTranslatedFields)
class IdeaWithTranslatedFieldsAdmin(admin.ModelAdmin):
    inlines = [IdeaTranslationsInline]

    fieldsets = [
        (
            _('Title and Content'),
            {'fields': ['title', 'content']}
        ),
        (
            _('Auhor and Category'),
            {'fields': ['author', 'categories']}
        )
    ]
