import importlib

from django.core.cache import cache
from django.test import testcases

from .decorators import override_persist_settings


class CacheTests(testcases.TestCase):

    def test_import_default_cache(self):
        imported = importlib.import_module('graphql_persist.cache')
        self.assertEqual(imported.cache, cache)

    @override_persist_settings(CACHE_NAME='not-found')
    def test_import_cache_error(self):
        imported = importlib.import_module('graphql_persist.cache')
        self.assertEqual(imported.cache, cache)
