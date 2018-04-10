
class DocumentDoesNotExist(Exception):

    def __init__(self, query_key):
        self.query_key = query_key
        return super().__init__(query_key)


class DocumentImportError(Exception):
    """Document Import Error"""
