"""
Define your app settings using the getattr() pattern in models.py
if you just have one or two settings, or in the app_settings.py
file if the settings are extensive and you want to organize
them better.
"""
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Example:
# SETTING_1 = getattr(settings, 'MAGAZINE_SETTING_1', 'default_value')
MEANING_OF_LIFE = getattr(settings, 'MAGAZINE_MEANING_OF_LIFE', 42)

ARTICLE_THEME_CHOICES = getattr(
    settings,
    'MAGAZINE_THEME_CHOICES',
    [
        ('futurism', _('Futurism')),
        ('nostalgia', _('Nostalgia')),
        ('sustainability', _('Sustainability')),
        ('wonder', _('Wonder'))
    ]
)
