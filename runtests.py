#!/usr/bin/env python
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'rapidsms_textit',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        ROOT_URLCONF='rapidsms_textit.tests.urls',
        INSTALLED_BACKENDS={
            'my-backend': {
                'ENGINE': 'rapidsms_textit.outgoing.TextItBackend',
                'config': {
                    "api_token": "de78a27456b82f8876e48d7ef339f75a1a6cfbd2",
                    "number": "+2348099890451",
                    "query_key": "key=somefunnystring"
                },
            }
        },
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': '/tmp/debug.log',
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
    )


# Note: We cannot import this until after the settings are configured,
# or Django throws a fit
from django.test.utils import get_runner


def runtests():

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    if 'test' in sys.argv[1:]:
        sys.argv.remove('test')
    args = sys.argv[1:] or ['rapidsms_textit', ]
    failures = test_runner.run_tests(args)
    sys.exit(failures)


if __name__ == '__main__':
    import logging

    root_logger = logging.getLogger('')
    # root_logger.setLevel(logging.DEBUG)
    # root_logger.addHandler(logging.StreamHandler())

    runtests()
