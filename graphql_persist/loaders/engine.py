from ..settings import persist_settings
from .base import Document
from .exceptions import DocumentDoesNotExist


class Engine:

    def __init__(self):
        self.dirs = persist_settings.DOCUMENTS_DIRS
        self.documents_ext = persist_settings.DOCUMENTS_EXT
        self.loaders = self.get_loaders()

    def get_document(self, query_key):
        return self.find_document(query_key)

    def from_string(self, document_code):
        return Document(document_code)

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
