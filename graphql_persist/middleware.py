import json

from django.utils.encoding import force_text

from graphene_django.views import GraphQLView

from .cache import get_persisted_query
from .settings import persist_settings


class PersistMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.document_id = None

    def __call__(self, request):
        response = self.get_response(request)
        response_handler = persist_settings.PERSISTED_RESPONSE_HANDLER

        if self.document_id is not None and response_handler is not None:
            response_handler(request, response, self.document_id)

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
                document_id = data.get('id', data.get('operationName'))

                if not data.get('query') and document_id:
                    query = get_persisted_query(document_id, request)

                    if query is not None:
                        data['query'] = query
                        request._body = json.dumps(data).encode()
                        self.document_id = document_id

        return None
