import os
import re

from django.core.cache import cache as default_cache
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from .settings import persist_settings

__all__ = [
    'query_key_handler',
    'get_persisted_query',
]

try:
    cache = caches[persist_settings.CACHE_NAME]
except (InvalidCacheBackendError, ValueError):
    cache = default_cache

versioning_regex = re.compile(r'\.([a-z])', re.IGNORECASE)


def query_key_handler(query_id, request):
    if request.version is None:
        return query_id

    query_prefix = versioning_regex.sub(r':\1', request.version)
    return ':'.join((query_prefix, query_id))


def get_query(query_key, file_name):
    with open(file_name, 'r') as document:
        query = document.read()
        cache_timeout = persist_settings.CACHE_TIMEOUT_HANDLER(query_key)
        cache.set(query_key, query, timeout=cache_timeout)
        return query


def get_persisted_query(query_id, request):
    query_key = persist_settings.QUERY_KEY_HANDLER(query_id, request)
    query = cache.get(query_key, None)

    if query is None:
        for document_dir in persist_settings.DOCUMENTS_DIRS:
            query_keys = query_key.split(':')

            for s in range(len(query_keys)):
                file_keys = query_keys[:-s - 1] + query_keys[-1:]
                file_name = os.path.join(document_dir, *file_keys)
                file_name += persist_settings.DOCUMENTS_EXT

                if os.path.isfile(file_name):
                    return get_query(query_key, file_name)
    return query
