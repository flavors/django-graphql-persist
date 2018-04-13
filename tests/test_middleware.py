import json
from unittest.mock import Mock

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.test import RequestFactory, override_settings, testcases

from graphene_django.views import GraphQLView

from graphql_persist import exceptions, versioning
from graphql_persist.middleware import PersistedQuery, PersistMiddleware
from graphql_persist.parser import parse_json
from graphql_persist.renderers import BaseRenderer
from graphql_persist.settings import persist_settings

from .decorators import override_persist_settings


class JSONRequestFactory(RequestFactory):

    def request(self, **request):
        return VersioningRequest(self._base_environ(**request))

    def post(self, path, data=None, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')

        if isinstance(data, dict):
            data = json.dumps(data)
        return super().post(path, data=data, *args, **kwargs)


class VersioningRequest(WSGIRequest):
    version = None


class Versioning(versioning.QueryParameterVersioning):
    allowed_versions = ('v1',)


class Renderer(BaseRenderer):

    def render(self, data, context=None):
        data['test'] = True
        return data


class MiddlewareTests(testcases.TestCase):

    def setUp(self):
        self.factory = JSONRequestFactory()
        self.get_response_mock = Mock(return_value=JsonResponse({}))
        self.middleware = PersistMiddleware(self.get_response_mock)
        self.view_func = GraphQLView.as_view()

    @override_settings(INSTALLED_APPS=['tests'])
    def test_process_view(self):
        data = {
            'id': 'schema',
        }

        request = self.factory.post('/', data=data)
        result = self.middleware.process_view(request, self.view_func)
        persisted_query = request.persisted_query
        document = persisted_query.document
        request_body = parse_json(request._body)

        self.assertIsNone(result)
        self.assertEqual(persisted_query.id, 'schema')
        self.assertEqual(document.origin.query_key._keys, ['schema'])
        self.assertEqual(document.source.body, request_body['query'])

    def test_process_unknown_view(self):
        request = self.factory.post('/')
        result = self.middleware.process_view(request, None)

        self.assertIsNone(result)

    def test_json_decode_error(self):
        request = self.factory.post('/', data='error')
        result = self.middleware.process_view(request, self.view_func)

        self.assertIsNone(result)

    @override_settings(INSTALLED_APPS=['tests'])
    def test_syntax_error(self):
        data = {
            'id': 'syntax_error',
        }

        request = self.factory.post('/', data=data)
        result = self.middleware.process_view(request, self.view_func)

        self.assertIsInstance(result, exceptions.DocumentSyntaxError)

    def test_document_not_found(self):
        data = {
            'id': 'not-found',
        }

        request = self.factory.post('/', data=data)
        result = self.middleware.process_view(request, self.view_func)

        self.assertIsInstance(result, exceptions.DocumentNotFound)

    def test_versioning_not_found(self):
        request = self.factory.post('/')
        response = self.middleware(request)

        self.assertIsNone(request.version)
        self.assertEqual(response.status_code, 200)

    @override_persist_settings(DEFAULT_VERSIONING_CLASS=Versioning)
    def test_versioning_not_allowed(self):
        middleware = PersistMiddleware(self.get_response_mock)

        request = self.factory.post('?{0}={1}'.format(
            persist_settings.VERSION_PARAM,
            'not-allowed'),
        )

        response = middleware(request)

        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, exceptions.PersistResponseError)

    @override_persist_settings(
        DEFAULT_RENDERER_CLASSES=(
            '{}.Renderer'.format(__name__),
        ),
    )
    def test_finalize_response(self):
        middleware = PersistMiddleware(self.get_response_mock)
        request = self.factory.post('/')
        request.persisted_query = PersistedQuery(None, {})

        response = middleware(request)
        data = parse_json(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['test'])

    def test_response_content_length(self):
        request = self.factory.post('/')
        content = '{}'

        response = HttpResponse(content)
        response['Content-Length'] = None

        self.middleware.finalize_response(request, response)
        self.assertEqual(response['Content-Length'], str(len(content)))
