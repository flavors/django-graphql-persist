import os

from django.utils._os import safe_join

from .base import BaseLoader, Origin
from .exceptions import DocumentDoesNotExist


class FilesystemLoader(BaseLoader):

    def get_dirs(self):
        return self.engine.dirs

    def get_sources(self, query_key):
        for document_dir in self.get_dirs():
            for s in range(len(query_key)):
                path = safe_join(document_dir, *query_key.qslice(-s))
                path += self.engine.documents_ext

                if os.path.isfile(path):
                    yield Origin(name=path, query_key=query_key, loader=self)

    def get_contents(self, origin):
        try:
            with open(origin.name) as document:
                return document.read()
        except FileNotFoundError:
            raise DocumentDoesNotExist(origin.query_key)
