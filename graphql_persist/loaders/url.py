import os

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

import requests

from .base import BaseLoader, Origin

__all__ = ['URLLoader']


class URLOrigin(Origin):

    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content


class URLLoader(BaseLoader):

    def get_dirs(self):
        return self.engine.dirs

    def get_sources(self, query_key):
        document_name = query_key + self.engine.documents_ext
        query_keys = document_name.split(':')

        for document_dir in self.get_dirs():
            origin_url = os.path.join(document_dir, *query_keys)

            try:
                URLValidator()(origin_url)
            except ValidationError:
                continue
            try:
                response = requests.get(origin_url)
            except requests.HTTPError:
                continue

            if response.status_code == 200:
                yield URLOrigin(
                    content=response.text,
                    name=origin_url,
                    query_key=query_key,
                    loader=self)

    def get_contents(self, origin):
        return origin.content
