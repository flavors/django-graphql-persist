from django.test import RequestFactory, testcases


class VersioningTestsCase(testcases.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.version = 'v1'
