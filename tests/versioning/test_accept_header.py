from graphql_persist import versioning
from graphql_persist.exceptions import GraphQLPersistError
from graphql_persist.settings import persist_settings

from .testcases import VersioningTestsCase


class AcceptHeaderVersioningTests(VersioningTestsCase):

    def test_get_version(self):
        headers = {
            'HTTP_ACCEPT': 'application/json; {0}={1}'.format(
                persist_settings.VERSION_PARAM,
                self.version),
        }

        request = self.request_factory.get('/', **headers)

        scheme = versioning.AcceptHeaderVersioning()
        scheme_version = scheme.get_version(request)

        self.assertEqual(scheme_version, self.version)

    def test_default_version(self):
        request = self.request_factory.get('/')

        scheme = versioning.AcceptHeaderVersioning()
        scheme.default_version = 'v2'
        scheme_version = scheme.get_version(request)

        self.assertEqual(scheme_version, scheme.default_version)

    def test_version_not_allowed(self):
        headers = {
            'HTTP_ACCEPT': 'application/json; {0}={1}'.format(
                persist_settings.VERSION_PARAM,
                self.version),
        }

        request = self.request_factory.get('/', **headers)

        scheme = versioning.AcceptHeaderVersioning()
        scheme.allowed_versions = ('v2',)

        with self.assertRaises(GraphQLPersistError):
            scheme.get_version(request)
