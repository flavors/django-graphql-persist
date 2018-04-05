from .base import BaseRenderer

__all__ = ['StripRelayTagsRenderer']


def strip_relay_tags(data):
    if isinstance(data, dict):
        edges = data.pop('edges', None)

        if edges is not None:
            results = strip_relay_tags(edges)

            if not data:
                return results

            data['results'] = results

        else:
            node = data.pop('node', None)

            if node is not None:
                return strip_relay_tags(node)

        ret = {}
        for k, v in data.items():
            ret[k] = strip_relay_tags(v)

    elif isinstance(data, list):
        ret = []
        for v in data:
            ret.append(strip_relay_tags(v))
    else:
        return data
    return ret


class StripRelayTagsRenderer(BaseRenderer):

    def render(self, data, context=None):
        return strip_relay_tags(data)
