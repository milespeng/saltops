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

ALLOWED_HOSTS = []

# Application definition

# CELERY_IMPORTS = ('saltjob.cron.scanHostJob',)
# CELERY_TIMEZONE = 'Asia/Shanghai'
INSTALLED_APPS = [
    'suit',
    'import_export',
    'common',
    'cmdb',
    'saltjob',
    'smart_selects',
    # 'jet.dashboard',
    # 'jet',
    'nested_inline',
    'mptt',
    'tools_manager',
    'rest_framework',
    'deploy_manager',
    'django_crontab',
    'dashboard',
    'django.contrib.admindocs',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'kombu.transport.django',
    'suit_dashboard',
    'debug_toolbar'
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

CRONJOBS = [
    ('*/30 * * * *', 'saltjob.cron.scanHostJob')
]

# 文件上传的路径
PACKAGE_PATH = "/Users/kira/oschina/saltops/doc/script/"
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
# JET_SIDE_MENU_COMPACT = True

# JET_SIDE_MENU_CUSTOM_APPS = [
#     ('cmdb', [
#         'IDCLevel',
#         'ISP',
#         'IDC',
#         'Cabinet',
#         'Rack',
#         'Host'
#     ]),
#     ('deploy_manager', [
#         'ProjectModule',
#         'Project',
#         'DeployJob'
#     ]),
#     # ('tools_manager', [
#     #     'ToolsTypes',
#     #     'ToolsScript',
#     # ]),
#     ('djcelery', [
#         'IntervalSchedule',
#         'CrontabSchedule',
#         'PeriodicTask',
#         'TaskState'
#
#     ]),
#     # ('kombu', [
#     #     'Message',
#     # ]),
# ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

SALT_REST_URL = 'http://192.168.80.133:8001/'
SALT_USER = 'loginsight'
SALT_PASSWORD = 'loginsight'

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_ALWAYS_EAGER = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

SUIT_CONFIG = {
    'ADMIN_NAME': "SaltOps",
    'MENU': (
        {'app': 'cmdb', 'icon': 'icon-leaf',
         'models': ('IDCLevel', 'ISP', 'IDC', 'Cabinet', 'Rack', 'Host')},
        {'app': 'deploy_manager', 'icon': 'icon-hdd',
         'models': ('ProjectModule', 'Project', 'DeployJob')},
        {'app': 'tools_manager', 'icon': 'icon-tasks',
         'models': ('ToolsTypes', 'ToolsScript', 'ToolsExecJob')},
        {'app': 'auth', 'icon': 'icon-lock', 'models': ('user', 'group')},
        {'app': 'djcelery', 'icon': 'icon-cog',
         'models': ('IntervalSchedule', 'CrontabSchedule', 'PeriodicTask', 'TaskState')},
    ),
    'LIST_PER_PAGE': 15
}

SALT_CONN_TYPE = 'http'  # http
SALT_HTTP_URL = 'http://192.168.80.133:5000'

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

INTERNAL_IPS=['127.0.0.1']