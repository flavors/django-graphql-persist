import re

__all__ = ['query_key_handler']

versioning_regex = re.compile(r'\.([a-z])', re.IGNORECASE)


def query_key_handler(query_id, request):
    if request.version is None:
        return query_id

    query_prefix = versioning_regex.sub(r':\1', request.version)
    return ':'.join((query_prefix, query_id))
