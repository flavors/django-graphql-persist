from django.test import testcases

from graphql_persist.query import QueryKey
from graphql_persist.settings import persist_settings


class QueryKeyTestsCase(testcases.TestCase):

    def setUp(self):
        self.query_key = QueryKey(['v1', 'full', 'schema'])
        self.path = '/'.join(self.query_key) + persist_settings.DOCUMENTS_EXT
