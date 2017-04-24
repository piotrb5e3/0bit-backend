from .base_settings import *

with open(os.path.join(BASE_DIR, 'backend/secretkey.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ALLOWED_HOSTS = ['www.0bit.pw', '0bit.pw']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '0bit-dev',
        'USER': '0bit-dev',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logging/0bit.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

RAVEN_CONFIG = {
    'dsn': 'https://xyz@127.0.0.1/123',
    'release': 'no-release',
}

CORS_ORIGIN_ALLOW_ALL = False
