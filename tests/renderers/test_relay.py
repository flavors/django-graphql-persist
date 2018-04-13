from django.test import testcases

from graphql_persist.renderers import StripRelayTagsRenderer


class RelayTests(testcases.TestCase):

    def setUp(self):
        self.renderer = StripRelayTagsRenderer()

    def test_strip_tags(self):
        data = {
            'edges': [{
                'node': True,
            }],
        }

        rendered = self.renderer.render(data)
        self.assertEqual(rendered, [True])

    def test_pagination_strip_tags(self):
        data = {
            'edges': [{
                'node': True,
            }],
            'pageInfo': {
                'startCursor': 'test',
            },
        }

        rendered = self.renderer.render(data)

        self.assertEqual(rendered['results'], [True])
        self.assertEqual(rendered['pageInfo']['startCursor'], 'test')
