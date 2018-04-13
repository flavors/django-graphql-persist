from .testcases import LoadersTestsCase


class EngineTests(LoadersTestsCase):

    def test_from_string(self):
        engine = self.engine_class()
        query = '{q}'
        document = engine.from_string(query)

        self.assertEqual(document.source.body, query)
