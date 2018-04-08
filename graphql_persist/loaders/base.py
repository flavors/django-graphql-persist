from .exceptions import DocumentDoesNotExist


class Origin:

    def __init__(self, name, query_key=None, loader=None):
        self.name = name
        self.query_key = query_key
        self.loader = loader

    def __str__(self):
        return self.name


class Document:

    def __init__(self, source, origin=None):
        self.source = source
        self.origin = origin

    def parse(self):
        return self.source


class BaseLoader:

    def __init__(self, engine, dirs=None):
        self.engine = engine

    def get_document(self, query_key):
        for origin in self.get_sources(query_key):
            try:
                contents = self.get_contents(origin)
            except DocumentDoesNotExist:
                continue
            return Document(source=contents, origin=origin)
        raise DocumentDoesNotExist(query_key)

    def get_sources(self, query_key):
        raise NotImplementedError('.get_sources() must be implemented')

    def get_contents(self, origin):
        raise NotImplementedError('.get_contents() must be implemented')
