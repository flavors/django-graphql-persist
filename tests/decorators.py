from django.test import override_settings


class override_persist_settings(override_settings):

    def __init__(self, **kwargs):
        super().__init__(GRAPHQL_PERSIST=kwargs)
