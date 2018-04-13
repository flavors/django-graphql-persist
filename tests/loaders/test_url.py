from unittest.mock import patch

import requests

from graphql_persist.loaders import DocumentDoesNotExist, URLLoader

from ..decorators import override_persist_settings
from .testcases import LoadersTestsCase


class MockResponse:

    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code


class URLTests(LoadersTestsCase):

    @patch('requests.get', side_effect=lambda url: MockResponse('', 200))
    @override_persist_settings(DOCUMENTS_DIRS=('https://example.com',))
    def test_get_document(self, *args):
        document = self.engine_class().get_document(self.query_key)
        origin = document.origin

        self.assertIsInstance(origin.loader, URLLoader)
        self.assertEqual(origin.query_key, self.query_key)
        self.assertIn(self.path, origin.name)

    @patch('requests.get', side_effect=requests.HTTPError())
    @override_persist_settings(DOCUMENTS_DIRS=('https://example.com',))
    def test_http_error(self, *args):

        with self.assertRaises(DocumentDoesNotExist):
            self.engine_class().get_document(self.query_key)

    @patch('requests.get', side_effect=lambda url: MockResponse('', 404))
    @override_persist_settings(DOCUMENTS_DIRS=('https://example.com',))
    def test_document_does_not_exist(self, *args):

        with self.assertRaises(DocumentDoesNotExist):
            self.engine_class().get_document(self.query_key)
