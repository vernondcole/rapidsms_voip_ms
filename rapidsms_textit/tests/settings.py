# simple settings file for test scripts

SITE_ID=1

SECRET_KEY = 'super-secretxxxxxxxx'

ROOT_URLCONF = 'rapidsms_textit.urls'

INSTALLED_BACKENDS = {
    'test-textit-backend': {
        'ENGINE': 'rapidsms_textit.outgoing.TextItBackend',
        'config': {
            "api_token": "de78a27456b82f8876e48d7ef339f75a1a6cfbd2",
            "number": "+2348099890451",
            "query_key": "key=MumbleMumble"  # this string must be sent as part of the URL from text.it
            # define our webhook URL like: http://vern-test.digvil.org/test_textit/?key=MumbleMumble
        },
    }
}

RAPIDSMS_HANDLERS = (
    'core.handlers.base.BaseHandler',
    'core.handlers.help.HelpHandler',
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'rapidsms_textit',
    # "rapidsms",
    # "rapidsms.backends.database",
    # "rapidsms.contrib.handlers",
    # "rapidsms.contrib.httptester",
    # "rapidsms.contrib.messagelog",
    # "rapidsms.contrib.messaging",
    # "rapidsms.contrib.registration",
    # "rapidsms.contrib.echo",
    # "rapidsms.contrib.default",  # Must be last
)

LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': '/tmp/textit_debug.log',
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'textit.views': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propigate': True,
                }
            },
        }
