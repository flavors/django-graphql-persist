from django.core.cache import cache as default_cache
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from .settings import persist_settings

try:
    cache = caches[persist_settings.CACHE_NAME]
except (InvalidCacheBackendError, ValueError):
    cache = default_cache
