from django.test import testcases

from graphql_persist.versioning import BaseVersioning


class VersioningNotImplementedError(BaseVersioning):
    """Versioning Not Implemented Error"""


class BaseTests(testcases.TestCase):

    def test_versioning_not_implemented_error(self):
        scheme = VersioningNotImplementedError()

        with self.assertRaises(NotImplementedError):
            scheme.get_version(None)
