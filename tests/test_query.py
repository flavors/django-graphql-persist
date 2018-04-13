from unittest.mock import Mock

from django.test import testcases

from graphql_persist.query import QueryKey, query_key_handler


class QueryTests(testcases.TestCase):

    def setUp(self):
        self.keys = ['v1', 'schema']
        self.query_key = QueryKey(self.keys)

    def test_query_key_handler_versioning(self):
        request_mock = Mock()
        request_mock.version = str(self.query_key[:-1])
        keys = query_key_handler(self.keys[-1], request_mock)

        self.assertEqual(keys, self.keys)

    def test_query_key_iter(self):
        self.assertEqual(next(iter(self.query_key)), self.keys[0])

    def test_query_key_len(self):
        self.assertEqual(len(self.query_key), len(self.keys))

    def test_query_key_getitem(self):
        self.assertEqual(self.query_key[0], self.keys[0])
        self.assertEqual(self.query_key[0:], self.query_key)

    def test_query_key_add(self):
        self.assertEqual(self.query_key + [], self.query_key)

    def test_query_key_repr(self):
        self.assertEqual(repr(self.query_key), repr(self.keys))

    def test_query_key_qslice(self):
        self.assertEqual(self.query_key.qslice(-1), self.query_key[1:])
