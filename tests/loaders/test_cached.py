from django.test import override_settings

from graphql_persist.loaders import CachedEngine

from ..testcases import QueryKeyTestsCase


class CachedTests(QueryKeyTestsCase):

    def setUp(self):
        super().setUp()
        self.engine_class = CachedEngine

    @override_settings(INSTALLED_APPS=['tests'])
    def test_get_document(self):
        engine = self.engine_class()
        document = engine.get_document(self.query_key)
        cached = engine.get_document_cache[str(self.query_key)]

        self.assertEqual(cached, document)

    def test_get_cached_document(self):
        engine = self.engine_class()
        engine.get_document_cache[str(self.query_key)] = True
        document = engine.get_document(self.query_key)

        self.assertTrue(document)

    @override_settings(INSTALLED_APPS=['tests'])
    def test_reset_cache(self):
        engine = self.engine_class()
        engine.get_document(self.query_key)
        engine.reset()

        self.assertFalse(engine.get_document_cache)
