import os
import sys
from dotenv import load_dotenv

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

load_dotenv()


def get_secret(setting):
    '''Get the secret variable or return explicit exception.'''
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
EXTERNAL_BASE = os.path.join(BASE_DIR, 'externals')
EXTERNAL_LIBS_PATH = os.path.join(EXTERNAL_BASE, 'libs')
EXTERNAL_APPS_PATH = os.path.join(EXTERNAL_BASE, 'apps')
sys.path = ['', EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')  # '_q%bu9n%vbw8_*44ckpcn^*%&(zfivo0c2rvvfuzi7)6m7eddk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
WEBSITE_URL = 'http://127.0.0.1:8000'

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    # contributed apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    # third-party apps
    'imagekit',
    # local apps
    'myproject.apps.core.apps.CoreAppConfig',  # Apps with mixins first!
    'myproject.apps.categories.apps.CategoriesConfig',
    'myproject.apps.ideas.apps.IdeasAppConfig',
    'myproject.apps.magazine.apps.MagazineAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'myproject', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DATABASE_NAME'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'
# LANGUAGES = [
#     ('bg', 'Bulgarian'), ('hr', 'Croatian'),
#     ('cs', 'Czech'), ('da', 'Danish'),
#     ('nl', 'Dutch'), ('en', 'English'),
#     ('et', 'Estonian'), ('fi', 'Finnish'),
#     ('fr', 'French'), ('de', 'German'),
#     ('el', 'Greek'), ('hu', 'Hungarian'),
#     ('ga', 'Irish'), ('it', 'Italian'),
#     ('lv', 'Latvian'), ('lt', 'Lithuanian'),
#     ('mt', 'Maltese'), ('pl', 'Polish'),
#     ('pt', 'Portuguese'), ('ro', 'Romanian'),
#     ('sk', 'Slovak'), ('sl', 'Slovene'),
#     ('es', 'Spanish'), ('sv', 'Swedish'),
#     ('kl', 'Klingonian')
# ]

LANGUAGES = [
    ('en', 'English'), ('ru', 'Russian'),
    ('fr', 'French'), ('de', 'German')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOCALE_PATH = [
    os.path.join(BASE_DIR, 'locale')
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myproject', 'site_static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# News Article Themes - rewrite app_settings
MAGAZINE_THEME_CHOICES = [
    ('futurism', _('Futurism')),
    ('nostalgia', _('Nostalgia')),
    ('sustainability', _('Sustainability')),
    ('wonder', _('Wonder')),
    ('positivity', _('Positivity')),
    ('solutions', _('Solutions')),
    ('science', _('Science')),
]

EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_PORT = get_secret('EMAIL_PORT')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
