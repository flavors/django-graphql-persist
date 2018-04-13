from django.test import override_settings

from graphql_persist.loaders import DocumentImportError
from graphql_persist.loaders.parser import parse_document

from .testcases import DocumentTestsCase


class ParserTests(DocumentTestsCase):

    def test_parse_no_imports(self):
        query = '{q}'
        document = self.get_document(query)
        parsed = parse_document(document)

        self.assertEqual(query, parsed)

    def test_import_document_not_found(self):
        query = '# from not-found import identifier\n{q}'
        document = self.get_document(query)

        with self.assertRaises(DocumentImportError):
            parse_document(document)

    @override_settings(INSTALLED_APPS=['tests'])
    def test_import_identifier_not_found(self):
        query = '# from .schema import not-found\n{q}'
        document = self.get_document(query)

        with self.assertRaises(DocumentImportError):
            parse_document(document)
