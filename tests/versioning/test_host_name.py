from django.test import override_settings

from graphql_persist import versioning
from graphql_persist.exceptions import GraphQLPersistError

from .testcases import VersioningTestsCase


class HostNameVersioningTests(VersioningTestsCase):

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_get_version(self):
        headers = {
            'HTTP_HOST': '{}.example.com'.format(self.version),
        }

        request = self.request_factory.get('/', **headers)

        scheme = versioning.HostNameVersioning()
        scheme_version = scheme.get_version(request)

        self.assertEqual(scheme_version, self.version)

    def test_default_version(self):
        request = self.request_factory.get('/')

        scheme = versioning.HostNameVersioning()
        scheme.default_version = 'v2'
        scheme_version = scheme.get_version(request)

        self.assertEqual(scheme_version, scheme.default_version)

    @override_settings(ALLOWED_HOSTS=['*'])
    def test_version_not_allowed(self):
        headers = {
            'HTTP_HOST': '{}.example.com'.format(self.version),
        }

        request = self.request_factory.get('/', **headers)

        scheme = versioning.HostNameVersioning()
        scheme.allowed_versions = ('v2',)

        with self.assertRaises(GraphQLPersistError):
            scheme.get_version(request)
