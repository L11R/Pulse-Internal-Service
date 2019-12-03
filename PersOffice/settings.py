"""
Django settings for PersOffice project.

Generated by 'django-admin startproject' using Django 1.10.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

config_path = os.path.join(BASE_DIR, 'conf.json')
DATA = dict()
with open(config_path, 'r') as f:
    DATA = json.load(f)
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DATA['SECRET_KEY']

CSRF_COOKIE_SECURE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'office.pulseexpress.ru', 'office.pochtomat.ru', 'office.pochtomat.tech']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Signin',
    'report',
    'ping',
    'parserapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

ROOT_URLCONF = 'PersOffice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PersOffice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATA['DB_NAME_DEFAULT'],
        'USER': DATA['DB_USER_DEFAULT'],
        'PASSWORD': DATA['DB_PASSWORD_DEFAULT'],
        'HOST': DATA['HOST_DEFAULT'],
        'PORT': DATA['PORT_DEFAULT'],
    },
    'report': {
        'NAME': DATA['DB_NAME_REPORT'],
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '{},{}'.format(DATA['HOST_REPORT'], DATA['PORT_REPORT']),
        'USER': DATA['DB_USER_REPORT'],
        'PASSWORD': DATA['DB_PASSWORD_REPORT'],
        'OPTIONS': {
            'host_is_server': True,
            'unicode_results': False,
        }
    }
}
os.environ['TDSVER'] = '8.0'
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

FILES_ROOT = os.path.join(BASE_DIR, 'report', 'files', 'xlsx')
FILES_URL = '/xslx'

REQUEST_FILES = os.path.join(BASE_DIR, 'Signin', 'files', 'excel_files')

MEDIA_ROOT = os.path.join(BASE_DIR, 'Signin', 'files', 'media')
MEDIA_URL = '/media/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')