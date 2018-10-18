from django.test import RequestFactory, testcases

from graphql_persist.query import QueryKey, query_key_handler


class QueryKeyTestCase(testcases.TestCase):

    def setUp(self):
        self.keys = ['v1', 'schema']
        self.query_key = QueryKey(self.keys)


class QueryKeyHandlerTests(QueryKeyTestCase):

    def setUp(self):
        super().setUp()
        self.request_factory = RequestFactory()

    def test_versioning(self):
        request = self.request_factory.get('/')
        request.version = str(self.query_key[:-1])
        keys = query_key_handler(self.keys[-1], request)

        self.assertEqual(keys, self.keys)


class QueryKeyTests(QueryKeyTestCase):

    def test_iter(self):
        self.assertEqual(next(iter(self.query_key)), self.keys[0])

    def test_len(self):
        self.assertEqual(len(self.query_key), len(self.keys))

    def test_getitem(self):
        self.assertEqual(self.query_key[0], self.keys[0])
        self.assertEqual(self.query_key[0:], self.query_key)

    def test_add(self):
        self.assertEqual(self.query_key + [], self.query_key)

    def test_repr(self):
        self.assertEqual(repr(self.query_key), repr(self.keys))

    def test_qslice(self):
        self.assertEqual(self.query_key.qslice(-1), self.query_key[1:])
