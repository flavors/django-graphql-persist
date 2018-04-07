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


class PersistedQueryNotFound(PersistResponseError):
    default_message = _('Persisted query not found')
    status_code = 404
