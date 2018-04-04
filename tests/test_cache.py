from django.test import testcases

from graphql_persist import cache
from graphql_persist.settings import persist_settings


class CacheTests(testcases.TestCase):

    def test_get_cache_key(self):
        cache_key = cache.get_cache_key('test', None)
        prefix = persist_settings.CACHE_KEY_PREFIX

        self.assertTrue(cache_key.startswith(prefix))
