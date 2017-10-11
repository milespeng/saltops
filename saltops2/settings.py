"""
Django settings for saltops2 project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8#(k1)9py0*)j6v92!w0fo0b!)v*%_c6&za&#7z(wv-r+e&(4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'suit',
    'smart_selects',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crontasks',
    'djcelery',
    'kombu.transport.django',
    'common',
    'cmdb',
    'nested_inline',
    'saltrest',
    'ops_tools',
    'suit_dashboard',
    'dashboard',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'import_export',
]
JQUERY_URL = False
USE_DJANGO_JQUERY = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SUIT = True
ROOT_URLCONF = 'saltops2.urls'

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

WSGI_APPLICATION = 'saltops2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
PACKAGE_PATH = "/home/kira/PycharmProjects/saltops2/scripts/"
STATIC_ROOT = 'static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    # ('admin', os.path.join(STATIC_ROOT, 'admin').replace('\\', '/')),
    # ('jet', os.path.join(STATIC_ROOT, 'jet').replace('\\', '/')),
    # ('range_filter', os.path.join(STATIC_ROOT, 'range_filter').replace('\\', '/')),
    # ('fonts', os.path.join(STATIC_ROOT, 'fonts').replace('\\', '/')),
    # ('plugins', os.path.join(STATIC_ROOT, 'plugins').replace('\\', '/')),

)
SUIT_CONFIG = {
    'ADMIN_NAME': "SaltOps2",
    'MENU': (
        {'app': 'cmdb', 'icon': 'icon-leaf',
         'models': ('IDCLevel', 'ISP', 'IDC', 'Cabinet', 'Rack', 'Host')},
        #     {'app': 'deploy_manager', 'icon': 'icon-hdd',
        #      'models': ('ProjectModule', 'Project', 'DeployJob')},
        {'app': 'ops_tools', 'icon': 'icon-tasks',
         'models': ('ToolsTypes', 'ToolsScript', 'ToolsExecJob')},
        {'app': 'auth', 'icon': 'icon-lock', 'models': ('user', 'group')},
        {'app': 'djcelery', 'icon': 'icon-cog',
         'models': ('IntervalSchedule', 'CrontabSchedule', 'PeriodicTask', 'TaskState')},
    ),
    'LIST_PER_PAGE': 15
}

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
djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
SALT_REST_URL = 'http://127.0.0.1:8001/'
SALT_USER = 'saltops'
SALT_PASSWORD = 'saltops'
