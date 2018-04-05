import json
from collections import OrderedDict

from django.utils.encoding import force_text

from graphene_django.views import GraphQLView

from .query import get_persisted_query
from .settings import persist_settings


class PersistMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.renderers = self.get_renderers()

    def __call__(self, request):
        response = self.get_response(request)

        if (response.status_code == 200 and
                hasattr(request, 'query_id') and
                self.renderers):

            self.render(request, response)

        return response

    def process_view(self, request, view_func, *args):
        if hasattr(view_func, 'view_class') and\
                issubclass(view_func.view_class, GraphQLView) and\
                request.content_type == 'application/json':

            try:
                data = json.loads(force_text(request.body))
            except json.JSONDecodeError:
                """"JSON Decode Error"""
            else:
                query_id = data.get('id', data.get('operationName'))

                if not data.get('query') and query_id:
                    query = get_persisted_query(query_id, request)

                    if query is not None:
                        data['query'] = query
                        request._body = json.dumps(data).encode()
                        request.query_id = query_id

        return None

    def get_renderers(self):
        renderer_classes = persist_settings.DEFAULT_RENDERER_CLASSES
        return [renderer() for renderer in renderer_classes]

    def render(self, request, response):
        content = force_text(response.content, encoding=response.charset)
        data = json.loads(content, object_pairs_hook=OrderedDict)

        context = {
            'request': request,
        }

        for renderer in self.renderers:
            data = renderer.render(data, context)

        response.content = json.dumps(data)

        if response.has_header('Content-Length'):
            response['Content-Length'] = str(len(content))
