import json
from collections import OrderedDict

from django.utils.encoding import force_text

from graphene_django.views import GraphQLView

from . import exceptions
from .query import get_persisted_query
from .settings import persist_settings

__all__ = ['PersistMiddleware']


def get_json_data(content, **kwargs):
    content = force_text(content, **kwargs)
    return json.loads(content, object_pairs_hook=OrderedDict)


class PersistMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.renderers = self.get_renderers()
        self.versioning_class = persist_settings.DEFAULT_VERSIONING_CLASS

    def __call__(self, request):
        try:
            request.version = self.get_version(request)
        except exceptions.GraphQLPersistError as err:
            return exceptions.PersistResponseError(str(err))

        response = self.get_response(request)

        if (response.status_code == 200 and
                hasattr(request, 'query_id') and
                self.renderers):

            self.finalize_response(request, response)
        return response

    def process_view(self, request, view_func, *args):
        if (hasattr(view_func, 'view_class') and
                issubclass(view_func.view_class, GraphQLView) and
                request.content_type == 'application/json'):

            try:
                data = get_json_data(request.body)
            except json.JSONDecodeError:
                return None

            query_id = data.get('id', data.get('operationName'))

            if query_id and not data.get('query'):
                persisted_query = get_persisted_query(query_id, request)

                if persisted_query is None:
                    return exceptions.PersistedQueryNotFound()

                data['query'] = persisted_query
                request.query_id = query_id
                request._body = json.dumps(data).encode()
        return None

    def get_version(self, request):
        if self.versioning_class is not None:
            return self.versioning_class().get_version(request)
        return None

    def get_renderers(self):
        renderer_classes = persist_settings.DEFAULT_RENDERER_CLASSES
        return [renderer() for renderer in renderer_classes]

    def finalize_response(self, request, response):
        data = get_json_data(response.content, encoding=response.charset)

        context = {
            'request': request,
        }

        for renderer in self.renderers:
            data = renderer.render(data, context)

        response.content = json.dumps(data)

        if response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))
