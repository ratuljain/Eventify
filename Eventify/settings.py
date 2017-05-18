"""
Django settings for Eventify project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import cloudinary
from pyfcm import FCMNotification

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$=mv1e5mpjk=1neb4g$3xqd_sdfb*hn-s55i=-)0a0qd31qt*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'lettuce.django',
    'eventify_api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jenkins',
    'rest_framework',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework.authtoken',
    'places',
    'rest_framework_swagger',
]

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'ratuljain1991@gmail.com'
# EMAIL_HOST_PASSWORD = ''

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Eventify.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Eventify.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eventify_api',
        'USER': 'deployer',
        'PASSWORD': 'fortheloveofgodpleaseuseagoodpassword',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_pylint',
    # 'django_jenkins.tasks.run_jslint',
    # 'django_jenkins.tasks.run_csslint',
    # 'django_jenkins.tasks.run_sloccount'
)

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     )
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    # 'PAGE_SIZE': 10
}

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
PROJECT_APPS = ('eventify_api',)

LETTUCE_APPS = (
    'eventify_api',
)

LETTUCE_TEST_SERVER = 'lettuce.django.server.DjangoServer'
LETTUCE_SERVER_PORT = 9000
LETTUCE_USE_TEST_DATABASE = True

UNIQUE_EMAIL = True

cloudinary.config(
    cloud_name="dukt9s7aj",
    api_key="742926962481883",
    api_secret="MQ5RQj650yZcaIhxC1IYcbnvSxg"
)

PLACES_MAPS_API_KEY = 'AIzaSyBqJsshdcMRAPeZIvzJ7YRBfENrdkwT4MA'

SERVICE_ACCOUNT_JSON_FILE = os.path.join(
    "eventify_api", "serviceAccountCredentials.json")

config = {
    "apiKey": "AIzaSyBOvqjUrM1juX2ZiPD1HwDQOjvKPY0q9nM",
    "authDomain": "eventifyapp-d5196.firebaseapp.com",
    "databaseURL": "https://eventifyapp-d5196.firebaseio.com/",
    "storageBucket": "eventifyapp-d5196.appspot.com",
    "serviceAccount": SERVICE_ACCOUNT_JSON_FILE
}

push_service = FCMNotification(api_key="AAAAaRIijwg:APA91bFhO7nK3uchPsKh8oo_WGzFwoL8hmfbfeWu"
                                       "_x5SBZqdm8nIcwsEAIg51qVt5l9rsajG4XlgeaBnuiUdFKoUuHve"
                                       "EEncH-2QozIA0VD2BYGhmnbnXnPjgbCHrpi3AAqK_E-RXhHGSZzaD"
                                       "D3lPhYXYffh4Pw-EQ")
