# -*- coding: utf-8 -*-
"""
Django settings for saltops project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7(9#4oty&&)!8==#p+*cpr9=3q_k_r@n%kti&k39smwtf)qrh$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.80.172', '127.0.0.1']

# Application definition
# CELERY_IMPORTS = ('saltjob.cron.scanHostJob',)
# CELERY_TIMEZONE = 'Asia/Shanghai'
INSTALLED_APPS = [
    # 'suit',
    'import_export',
    'common',
    'cmdb',
    'saltjob',
    'nested_inline',
    'mptt',
    'tools_manager',
    'rest_framework',
    'deploy_manager',
    'celery_manager',
    'base_auth',
    # 'dashboard',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'braces',
    'kombu.transport.django',
    # 'suit_dashboard',
    # 'debug_toolbar'
]

MIDDLEWARE = [
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'saltops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'saltops.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ('scripts', os.path.join(STATIC_ROOT, 'scripts').replace('\\', '/')),
    ('asserts', os.path.join(STATIC_ROOT, 'asserts').replace('\\', '/')),
    ('hplus', os.path.join(STATIC_ROOT, 'hplus').replace('\\', '/')),
    ('admin', os.path.join(STATIC_ROOT, 'admin').replace('\\', '/')),
    ('djcelery', os.path.join(STATIC_ROOT, 'djcelery').replace('\\', '/')),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ('mptt', os.path.join(STATIC_ROOT, 'mptt').replace('\\', '/')),
    ('range_filter', os.path.join(STATIC_ROOT, 'range_filter').replace('\\', '/')),
    ('rest_framework', os.path.join(STATIC_ROOT, 'rest_framework').replace('\\', '/')),

)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

SALT_HTTP_URL = 'http://127.0.0.1:32769'
PACKAGE_PATH = "/Users/kira/opensource/saltops/static/scripts/"
SALT_REST_URL = 'http://127.0.0.1:32768/'
SALT_USER = 'ops'
SALT_PASSWORD = '123456'
SALT_CONN_TYPE = 'http'  # http
# SALT_HTTP_URL = 'http://127.0.0.1:5000'
# PACKAGE_PATH = "/home/kira/code/saltops/static/scripts/"
# SALT_REST_URL = 'http://127.0.0.1:8001/'
# SALT_USER = 'saltops'
# SALT_PASSWORD = 'saltops'

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)s [ %(message)s] %(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
        # 'file_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'filename': '',
        #     'formatter': 'standard'
        # },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

DEFAULT_LOGGER = 'default'

CORS_ORIGIN_ALLOW_ALL = True
LOGIN_URL = "/"
PER_PAGE = 10
