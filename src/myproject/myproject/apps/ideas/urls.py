from django.urls import path

from .views import (
    IdeaWithTranslatedFieldsDetailView,
    IdeaWithTranslatedFieldsListView,
    create_or_update_idea_view,
    delete_idea_view
)

app_name = 'ideas'

urlpatterns = [
    path(
        '',
        IdeaWithTranslatedFieldsListView.as_view(),
        name='idea_list'
    ),
    path(
        'add/',
        create_or_update_idea_view,
        name='create_idea'
    ),
    path(
        '<uuid:pk>/',
        IdeaWithTranslatedFieldsDetailView.as_view(),
        name='idea_detail'
    ),
    path(
        '<uuid:pk>/change/',
        create_or_update_idea_view,
        name='change_idea'
    ),
    path(
        '<uuid:pk>/delete/',
        delete_idea_view,
        name='delete_idea'
    )
]
