from graphql_persist.loaders.base import Document, Origin
from graphql_persist.settings import persist_settings

from ..testcases import QueryKeyTestsCase


class LoadersTestsCase(QueryKeyTestsCase):

    def setUp(self):
        super().setUp()
        self.engine_class = persist_settings.DEFAULT_LOADER_ENGINE_CLASS


class DocumentTestsCase(LoadersTestsCase):

    def setUp(self):
        super().setUp()
        self.loader = self.engine_class().get_loaders()[0]
        self.origin = Origin(self.path, self.query_key, self.loader)

    def get_document(self, source):
        return Document(source, origin=self.origin)
