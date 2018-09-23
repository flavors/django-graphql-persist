import re

__all__ = ['query_key_handler']


versioning_regex = re.compile(r'\.(?!\d)')


def query_key_handler(query_id, request):
    query_key = query_id.split(':')

    if request.version is None:
        return query_key

    versioning_prefix = versioning_regex.split(request.version)
    return versioning_prefix + query_key


class QueryKey:

    def __init__(self, keys):
        self._keys = keys

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, index):
        value = self._keys[index]
        if isinstance(index, slice):
            return type(self)(value)
        return value

    def __eq__(self, other):
        return self._keys == other._keys

    def __add__(self, keys):
        return type(self)(self._keys + keys)

    def __repr__(self):
        return list.__repr__(self._keys)

    def __str__(self):
        return '.'.join(self._keys)

    def qslice(self, end):
        return self[:end - 1] + self[-1:]._keys
