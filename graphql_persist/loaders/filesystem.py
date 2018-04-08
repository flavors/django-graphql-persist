import os

from django.utils._os import safe_join

from .base import BaseLoader, Origin
from .exceptions import DocumentDoesNotExist


class FilesystemLoader(BaseLoader):

    def get_dirs(self):
        return self.engine.dirs

    def get_sources(self, query_key):
        document_name = query_key + self.engine.documents_ext
        query_keys = document_name.split(':')

        for document_dir in self.get_dirs():
            for s in range(len(query_keys)):
                origin_keys = query_keys[:-s - 1] + query_keys[-1:]
                origin_path = safe_join(document_dir, *origin_keys)

                if os.path.isfile(origin_path):
                    yield Origin(
                        name=origin_path,
                        query_key=query_key,
                        loader=self)

    def get_contents(self, origin):
        try:
            with open(origin.name, 'r') as document:
                return document.read()
        except FileNotFoundError:
            raise DocumentDoesNotExist(origin)
