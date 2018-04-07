from collections import OrderedDict

from .base import BaseStripTagsRenderer

__all__ = ['StripRelayTagsRenderer']


def strip_edges(data):
    if isinstance(data, dict):
        edges = data.get('edges')
        if edges is not None:
            if len(data) == 1:
                return edges
            return OrderedDict(
                ('results', edges) if k == 'edges'
                else (k, v) for k, v in data.items())
        elif 'node' in data:
            return data['node']
    return data


class StripRelayTagsRenderer(BaseStripTagsRenderer):
    strip_func = staticmethod(strip_edges)
