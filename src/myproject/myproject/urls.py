"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from myproject.apps.ideas.views import idea_detail_view

urlpatterns = i18n_patterns(
    path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    path('ideas/<int:idea_id>/', idea_detail_view, name='idea-detail'),
    path(
        'translated-ideas/',
        include(
            'myproject.apps.ideas.urls',
            namespace='ideas'
        )
    ),
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    )
)
# urlpatterns = [
#     path('', TemplateView.as_view(template_name="index.html")),
#     path('admin/', admin.site.urls),
#     path('ideas/<int:idea_id>/', idea_detail_view, name='idea-detail')
# ]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
