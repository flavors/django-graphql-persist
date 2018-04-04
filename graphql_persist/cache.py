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


def get_cache_key(document_id, request):
    cache_key = persist_settings.CACHE_KEY_HANDLER(document_id, request)
    return ':'.join((persist_settings.CACHE_KEY_PREFIX, cache_key))


def set_cache_key(document_dir, dirpath, filename):
    return ':'.join((
        persist_settings.CACHE_KEY_PREFIX,
        os.path.relpath(dirpath, document_dir).replace('/', ':'),
        os.path.splitext(filename)[0]),
    )


def get_query(cache_key, dirpath, filename):
    with open(os.path.join(dirpath, filename)) as file:
        query = file.read()
        cache_timeout = persist_settings.CACHE_TIMEOUT
        cache.set(cache_key, query, timeout=cache_timeout)
        return query


def get_persisted_query(document_id, request):
    cache_key = get_cache_key(document_id, request)
    query = cache.get(cache_key, None)

    if query is None:
        for document_dir in persist_settings.DOCUMENTS_DIRS:
            for dirpath, _, _ in os.walk(document_dir):
                filename = document_id + '.graphql'

                if cache_key == set_cache_key(document_dir, dirpath, filename):
                    return get_query(cache_key, dirpath, filename)
    return query
