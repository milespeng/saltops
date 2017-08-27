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
            'format': '[ %(message)s]  %(pathname)s  %(funcName)s %(lineno)d'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'INFO',
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
            'propagate': True,
            'formatter': 'standard'
        }
    }
}
