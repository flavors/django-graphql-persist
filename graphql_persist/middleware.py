import json

from graphene_django.views import GraphQLView
from graphql.error import GraphQLSyntaxError

from . import exceptions
from .loaders import DocumentDoesNotExist, DocumentImportError
from .parser import parse_json
from .query import QueryKey
from .settings import persist_settings

__all__ = ['PersistMiddleware']


class PersistedQuery(dict):

    def __init__(self, document, data):
        super().__init__(data)
        self.__dict__ = self
        self.document = document


class PersistMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.loader = persist_settings.DEFAULT_LOADER_ENGINE_CLASS()
        self.renderers = self.get_renderers()
        self.versioning_class = persist_settings.DEFAULT_VERSIONING_CLASS

    def __call__(self, request):
        try:
            request.version = self.get_version(request)
        except exceptions.GraphQLPersistError as e:
            return exceptions.PersistResponseError(str(e))

        response = self.get_response(request)

        if (response.status_code == 200 and
                hasattr(request, 'persisted_query') and
                self.renderers):

            self.finalize_response(request, response)
        return response

    def process_view(self, request, view_func, *args):
        if (hasattr(view_func, 'view_class') and
                issubclass(view_func.view_class, GraphQLView) and
                request.content_type == 'application/json'):

            try:
                data = parse_json(request.body)
            except ValueError:
                return None

            query_id = data.get('id', data.get('operationName'))

            if query_id and not data.get('query'):
                query_key = self.get_query_key(query_id, request)

                try:
                    document = self.loader.get_document(query_key)
                except DocumentDoesNotExist:
                    return exceptions.DocumentNotFound(query_key)
                try:
                    data['query'] = document.render()
                except (DocumentImportError, GraphQLSyntaxError) as e:
                    return exceptions.DocumentSyntaxError(str(e))

                request.persisted_query = PersistedQuery(document, data)
                request._body = json.dumps(data).encode()
        return None

    def get_query_key(self, query_id, request):
        return QueryKey(persist_settings.QUERY_KEY_HANDLER(query_id, request))

    def get_version(self, request):
        if self.versioning_class is not None:
            return self.versioning_class().get_version(request)
        return None

    def get_renderers(self):
        renderer_classes = persist_settings.DEFAULT_RENDERER_CLASSES
        return [renderer() for renderer in renderer_classes]

    def finalize_response(self, request, response):
        data = parse_json(response.content, encoding=response.charset)

        context = {
            'request': request,
        }

        for renderer in self.renderers:
            data = renderer.render(data, context)

        response.content = json.dumps(data)

        if response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))
