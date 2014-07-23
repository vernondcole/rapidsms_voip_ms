import mock

from .utils import TextItTest,  BACKEND_NAME


class TextItSendTest(TextItTest):

    def test_send(self):
        # send method passes a reasonable TextIt program to
        # execute_textit_program
        backend = self.router.backends[BACKEND_NAME]
        config = self.get_config()
        FROM = config['number']
        text = u"MESSAGE\u0123\u0743"
        with mock.patch.object(backend, 'execute_textit_program') as execute:
            backend.send(None, text, ["id1", "id2"])
        execute.assert_called()
        args, kwargs = execute.call_args
        program = args[0]
        expected_program = {
            'textit': [
                {
                    'message': {
                        'say': {'value': text},
                        'to': "id1",
                        'from': FROM,
                        'channel': 'TEXT',
                        'network': 'SMS',
                    }
                },
                {
                    'message': {
                        'say': {'value': text},
                        'to': "id2",
                        'from': FROM,
                        'channel': 'TEXT',
                        'network': 'SMS',
                    }
                }
            ]
        }
        self.assertEqual(expected_program, program)
