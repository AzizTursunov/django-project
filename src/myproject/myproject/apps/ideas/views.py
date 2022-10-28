from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import Idea, IdeaWithTranslatedFields


def idea_detail_view(request, idea_id=None):
    idea = get_object_or_404(Idea, id=idea_id)
    is_translated = False
    template_name = 'ideas/idea-detail.html'
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
    template_name = 'ideas/idea-detail.html'
    is_translated = True
    context = {
        'title': 'Idea detail',
        'object': idea,
        'is_translated': is_translated

    }
    return render(request, template_name, context)
