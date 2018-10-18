import json

from django.test import RequestFactory, testcases

from graphql_persist import parser


class ParserTests(testcases.TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_application_json(self):
        request = self.request_factory.post(
            '/',
            data=json.dumps({'test': True}),
            content_type='application/json')

        result = parser.parse_body(request)
        self.assertTrue(result['test'])

    def test_json_decode_error(self):
        request = self.request_factory.post(
            '/',
            data='error',
            content_type='application/json')

        result = parser.parse_body(request)
        self.assertIsNone(result)

    def test_x_www_form_urlencoded(self):
        request = self.request_factory.post('/', data={'test': True})
        result = parser.parse_body(request)

        self.assertTrue(eval(result['test']))

    def test_unknown_content_type(self):
        request = self.request_factory.post(
            '/',
            data={'test': True},
            content_type='unknown')

        result = parser.parse_body(request)
        self.assertIsNone(result)
