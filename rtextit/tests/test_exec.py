# Tests for execute_textit_program
from __future__ import print_function   # ToDo , unicode_literals
import json

from django.core import signing

import mock

from .utils import TextItTest, BACKEND_NAME


class TestExecute(TextItTest):

    def test_execute(self):
        # The execute_program method on the backend passes the signed
        # program to post.   # ToDo: Any unicode is preserved too.
        program = [{'one': 1, 'two': "mumble, mumble"}]   # ToDo "Unicode \u0123\u4321"}]

        result = {
            'success': True,
        }
        mock_response = mock.Mock(status_code=200, content=json.dumps(result))
        with mock.patch('requests.post') as post:
            post.return_value = mock_response
            self.router.backends[BACKEND_NAME].textit_post('xxx', program)
        post.assert_called()
        args, kwargs = post.call_args
        print('post.call_args={!r}'.format(args)) ###
        endpoint = args[0].rsplit('/', 1)[1]
        # print('endpoint="{}"'.format(endpoint))
        self.assertEquals(endpoint, 'xxx.json')
        print('msg type={}, kwargs={!r}'.format(type(kwargs), kwargs)) ###
        authorization = kwargs['auth']
        class x():
            def __init__(self):
                self.headers = {}
        self.assertEqual(authorization(x()).headers['Token'], self.get_config()['api_token'])
        msg = json.loads(kwargs['data'])
        self.assertEqual(msg, program)
