import json
import logging

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from rapidsms.backends.base import BackendBase

import requests
from requests.auth import AuthBase

class TokenAuth(AuthBase):
    """ special "Token" authentication for TextIt """
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers['Token'] = self.token
        return r
    def __repr__(self):
        return '<TokenAuth=Token {}>'.format(self.token)

logger = logging.getLogger(__name__)

base_url = 'https://api.textit.in/api/v1/{}.json'


class TextItBackend(BackendBase):
    """A RapidSMS backend for TextIt"""

    def configure(self, config=None, **kwargs):
        """
        We expect all of our config (apart from the ENGINE) to be
        in a dictionary called 'config' in our INSTALLED_BACKENDS entry
        """
        self.config = config or {}
        for key in ['api_token', 'number']:
            if key not in self.config:
                msg = "TextIt backend config must set '%s'; config is %r" %\
                      (key, config)
                raise ImproperlyConfigured(msg)
        if kwargs:
            msg = "All textit backend config should be within the `config`"\
                "entry of the backend dictionary"
            raise ImproperlyConfigured(msg)

    @property
    def token(self):
        return self.config['api_token']

    def textit_post(self, endpoint, params):
        """
        Ask TextIt to execute a program for us using a POST

        See http://textit.in/api/v1
        for the format we're using to call TextIt, pass it data, and ask
        them to call us back.

        :param endpoint: the TextIt endpoint name: i.e.: "sms", "contacts", etc.
        :param params: A TextIt program, i.e. a dictionary containing the
             parameters for our JSON call.
        """
        data = json.dumps(params)

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        response = requests.post(base_url.format(endpoint),
                                 data=data,
                                 headers=headers,
                                 auth=TokenAuth(self.token))

        # If the HTTP request failed, raise an appropriate exception - e.g.
        # if our network (or TextIt) are down:
        response.raise_for_status()

        result = response.json()
        print('response was={!r}'.format(response))  ###
        print('result was={!r}'.format(result))  ###


    def send(self, id_, text, identities, context=None):
        """
        Send messages when using RapidSMS 0.14.0 or later.

        We can send multiple messages in one TextIt program, so we do
        that.

        :param id_: Unused, included for compatibility with RapidSMS.
        :param string text: The message text to send.
        :param identities: A list of identities to send the message to
            (a list of strings)
        :param context: Unused, included for compatibility with RapidSMS.
        """

        # Build our program
        program = {
                'phone': identities,
                'text': text
            }
        self.textit_post('sms', program)
