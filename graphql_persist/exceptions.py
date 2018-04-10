from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _


class GraphQLPersistError(Exception):
    """GraphQL Persist Error"""


class PersistResponseError(JsonResponse):
    default_message = _('A server error occurred')
    status_code = 400

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        return super().__init__({
            'errors': [{'message': message}],
        })


class DocumentNotFound(PersistResponseError):
    status_code = 404

    def __init__(self, query_key):
        message = _('Document `{}` not found').format(query_key)
        return super().__init__(message)


class DocumentSyntaxError(PersistResponseError):
    """Document Syntax Error"""
