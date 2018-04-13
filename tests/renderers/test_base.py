from django.test import testcases

from graphql_persist.renderers import BaseRenderer, BaseStripTagsRenderer
from graphql_persist.renderers.base import strip_tags


class RendererNotImplementedError(BaseRenderer):
    """Renderer Not Implemented Error"""


class StripTagsRendererError(BaseStripTagsRenderer):
    """Strip Tags Renderer Error"""


class BaseTests(testcases.TestCase):

    def test_renderer_not_implemented_error(self):
        renderer = RendererNotImplementedError()

        with self.assertRaises(NotImplementedError):
            renderer.render({})

    def test_strip_tags_renderer_error(self):
        renderer = StripTagsRendererError()

        with self.assertRaises(Exception):
            renderer.render({})

    def test_strip_tags(self):
        data = {
            'results': [{
                'test': True,
            }],
        }

        def strip_func(data):
            if isinstance(data, dict):
                if 'test' in data:
                    return data['test']
            return data

        rendered = strip_tags(data, strip_func)
        self.assertEqual(rendered['results'], [True])
