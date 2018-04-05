from django.test import testcases

from graphql_persist import query
from graphql_persist.settings import persist_settings


class QueryTests(testcases.TestCase):

    def test_get_cache_key(self):
        query_key = query.get_cache_key('test')
        prefix = persist_settings.CACHE_KEY_PREFIX

        self.assertTrue(query_key.startswith(prefix))
