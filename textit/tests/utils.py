from django.conf import settings

from rapidsms.tests.harness import RapidTest

class TextItTest(RapidTest):
    # Override TestRouter's override of the backends
    backends = settings.INSTALLED_BACKENDS

    def get_config(self):
        return settings.INSTALLED_BACKENDS['textit-backend']['config']
