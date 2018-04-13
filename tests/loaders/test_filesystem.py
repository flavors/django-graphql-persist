from pathlib import Path
from unittest.mock import patch

from graphql_persist.loaders import DocumentDoesNotExist, FilesystemLoader
from graphql_persist.settings import persist_settings

from ..decorators import override_persist_settings
from .testcases import LoadersTestsCase

documents_dir = (
    Path(__file__).parents[1] /
    persist_settings.APP_DOCUMENT_DIR
).as_posix()


class FilesystemTests(LoadersTestsCase):

    @override_persist_settings(DOCUMENTS_DIRS=(documents_dir,))
    def test_get_document(self):
        document = self.engine_class().get_document(self.query_key)
        origin = document.origin

        self.assertIsInstance(origin.loader, FilesystemLoader)
        self.assertEqual(origin.query_key, self.query_key)
        self.assertIn(self.path, origin.name)

    @patch('graphql_persist.loaders.filesystem.open')
    @override_persist_settings(DOCUMENTS_DIRS=(documents_dir,))
    def test_document_does_not_exist(self, open_mock):
        open_mock.side_effect = FileNotFoundError()

        with self.assertRaises(DocumentDoesNotExist):
            self.engine_class().get_document(self.query_key)
