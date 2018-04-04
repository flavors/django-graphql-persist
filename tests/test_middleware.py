from unittest.mock import Mock

from django.http import JsonResponse
from django.test import RequestFactory, testcases

from graphene_django.views import GraphQLView

from graphql_persist.middleware import PersistMiddleware


class MiddlewareTests(testcases.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.get_response_mock = Mock(return_value=JsonResponse({}))
        self.middleware = PersistMiddleware(self.get_response_mock)
        self.view_func = GraphQLView.as_view()

    def test_process_view(self, *args):
        request = self.factory.post('/', content_type='application/json')

        self.middleware.process_view(request, self.view_func)
