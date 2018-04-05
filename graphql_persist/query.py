import os

from django.core.cache import cache as default_cache
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from .settings import persist_settings

try:
    cache = caches[persist_settings.CACHE_NAME]
except (InvalidCacheBackendError, ValueError):
    cache = default_cache


__all__ = ['get_persisted_query']


def get_file_key(document_dir, dirpath, filename):
    return ':'.join((
        os.path.relpath(dirpath, document_dir).replace('/', ':'),
        os.path.splitext(filename)[0]),
    )


def get_query(query_key, dirpath, filename):
    with open(os.path.join(dirpath, filename)) as file:
        query = file.read()
        cache_timeout = persist_settings.CACHE_TIMEOUT_HANDLER(query_key)
        cache.set(query_key, query, timeout=cache_timeout)
        return query


def get_persisted_query(query_id, request):
    query_key = persist_settings.QUERY_KEY_HANDLER(query_id, request)
    query = cache.get(query_key, None)

    if query is None:
        for document_dir in persist_settings.DOCUMENTS_DIRS:
            for dirpath, _, filenames in os.walk(document_dir):
                filename = query_id + '.graphql'

                if filename not in filenames:
                    continue

                if query_key == get_file_key(document_dir, dirpath, filename):
                    return get_query(query_key, dirpath, filename)
    return query
