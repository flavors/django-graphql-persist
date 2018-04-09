from .engine import Engine


class CachedEngine(Engine):

    def __init__(self):
        super().__init__()
        self.get_document_cache = {}

    def get_document(self, query_key):
        document = self.get_document_cache.get(query_key)

        if document is None:
            document = self.find_document(query_key)
            self.get_document_cache[query_key] = document
        return document

    def reset(self):
        self.get_document_cache.clear()
