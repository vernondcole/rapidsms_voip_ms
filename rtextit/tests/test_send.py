import mock

from .utils import TextItTest


class TextItSendTest(TextItTest):

    def test_send(self):
        # send method passes needed TextIt commands to textit_post.
        backend = self.router.backends['textit-backend']
        config = self.get_config()
        FROM = config['number']
        text = u"MESSAGE\u0123\u0743"
        with mock.patch.object(backend, 'textit_post') as execute:
            backend.send(None, text, ["id1", "id2"])
        execute.assert_called()
        args, kwargs = execute.call_args
        self.assertEqual(args[0], 'sms')
        program = args[1]
        expected_program = {
            'phone': ["id1", "id2"],
            'text': text
        }
        self.assertEqual(expected_program, program)
