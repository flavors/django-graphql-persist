from ..settings import persist_settings
from .exceptions import DocumentDoesNotExist


class CachedEngine:
    dirs = persist_settings.DOCUMENTS_DIRS
    documents_ext = persist_settings.DOCUMENTS_EXT

    def __init__(self, dirs=None):
        self.get_document_cache = {}
        self.loaders = self.get_loaders()

    def get_document(self, query_id, request):
        query_key = persist_settings.QUERY_KEY_HANDLER(query_id, request)
        document = self.get_document_cache.get(query_key)

        if document is None:
            document = self.find_document(query_key)
            self.get_document_cache[query_key] = document
        return document

    def find_document(self, query_key):
        for loader in self.loaders:
            try:
                return loader.get_document(query_key)
            except DocumentDoesNotExist:
                continue
        raise DocumentDoesNotExist(query_key)

    def get_loaders(self):
        loader_classes = persist_settings.DEFAULT_LOADER_CLASSES
        return [loader_class(self) for loader_class in loader_classes]

    def get_sources(self, query_key):
        for loader in self.loaders:
            yield from loader.get_sources(query_key)

    def reset(self):
        self.get_document_cache.clear()
