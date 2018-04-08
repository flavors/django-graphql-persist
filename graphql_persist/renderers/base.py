from collections import OrderedDict

__all__ = [
    'BaseRenderer',
    'BaseStripTagsRenderer',
]


def strip_tags(data, f):
    data = f(data)
    if isinstance(data, dict):
        return OrderedDict(
            (k, strip_tags(v, f))
            for k, v in data.items())
    elif isinstance(data, list):
        return [strip_tags(v, f) for v in data]
    return data


class BaseRenderer:

    def render(self, data, context=None):
        raise NotImplementedError('.render() must be implemented')


class BaseStripTagsRenderer:

    def render(self, data, context=None):
        assert hasattr(self, 'strip_func'), (
            '`{cls}.strip_func` argument is required'
            .format(cls=self.__class__.__name__)
        )
        return strip_tags(data, self.strip_func)
