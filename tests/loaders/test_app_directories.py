from django.test import override_settings

from graphql_persist.loaders import AppDirectoriesLoader, DocumentDoesNotExist

from .testcases import LoadersTestsCase


class AppDirectoriesTests(LoadersTestsCase):

    @override_settings(INSTALLED_APPS=['tests'])
    def test_get_document(self):
        document = self.engine_class().get_document(self.query_key)
        origin = document.origin

        self.assertIsInstance(origin.loader, AppDirectoriesLoader)
        self.assertEqual(origin.query_key, self.query_key)
        self.assertIn(self.path, origin.name)

    def test_document_does_not_exist(self):
        with self.assertRaises(DocumentDoesNotExist):
            self.engine_class().get_document(self.query_key)
