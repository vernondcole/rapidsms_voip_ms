from __future__ import print_function, unicode_literals
import json
import logging

import mock

from django.core.urlresolvers import reverse

from .utils import TextItTest


logger = logging.getLogger(__name__)


class TextItViewTest(TextItTest):

    disable_phases = True

    def send_to_view(self, data):
        """Send data to the textit view, return whatever the response is"""
        encoded_data = {u'status': u'P', u'direction': u'I', u'phone': u'+' + data['phone'],
                        u'text': data['text'], u'sms': u'449177', u'relayer': u'2166',
                        u'time': u'2014-08-04T17:05:16.000000', u'relayer_phone': u'+23480998904',
                        u'event': data['event']}
        url = reverse('textit-backend') + '?key=somefunnystring'
        return self.client.post(url, encoded_data)

    def test_cannot_get(self):
        # GET is not a valid method
        response = self.client.get(reverse('textit-backend'))
        self.assertEqual(405, response.status_code)

    def test_invalid_response(self):
        """HTTP 400 should return if data is invalid."""
        data = {'event': 'illegal', 'phone': '42', 'text': 'hi there'}
        conn = mock.Mock()
        with mock.patch('rapidsms_textit.views.lookup_connections') as \
                lookup_connections:
            lookup_connections.return_value = [conn]
            with mock.patch('rapidsms_textit.views.receive') as receive:
                response = self.send_to_view(data)
        self.assertEqual(response.status_code, 400)
        receive.assert_called()

    def test_incoming_message(self):
        # If we call the view as if TextIt is delivering a message, the
        # message is passed to RapidSMS. Any unicode is preserved.
        text = u"TEXT MESSAGE \u0123\u4321"
        data = {
            'event': 'mo_sms',
            'phone': '42',
            'text': text,
        }
        conn = mock.Mock()
        with mock.patch('rapidsms_textit.views.lookup_connections') as \
                lookup_connections:
            lookup_connections.return_value = [conn]
            with mock.patch('rapidsms_textit.views.receive') as receive:
                response = self.send_to_view(data)
        self.assertEqual(200, response.status_code, response.content)
        receive.assert_called()
        args, kwargs = receive.call_args
        received_text, connection = args
        self.assertEqual(text, received_text)
        self.assertEqual(conn, connection)
