from graphql_persist.loaders import BaseLoader

from .testcases import DocumentTestsCase


class LoaderNotImplementedError(BaseLoader):
    """Loader Not Implemented Error"""


class BaseTests(DocumentTestsCase):

    def test_origin_str(self):
        self.assertEqual(str(self.origin), self.origin.name)

    def test_document_render(self):
        query = '{q}'
        rendered = self.get_document(query).render()

        self.assertEqual(rendered, query)

    def test_loader_not_implemented_error(self):
        engine = self.engine_class()
        loader = LoaderNotImplementedError(engine)

        with self.assertRaises(NotImplementedError):
            loader.get_sources(self.query_key)

        with self.assertRaises(NotImplementedError):
            loader.get_contents(self.origin)
