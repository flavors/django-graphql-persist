
class DocumentDoesNotExist(Exception):
    """Document Does Not Exist"""


class DocumentSyntaxError(Exception):

    def __init__(self, query_key, syntax_error=None):
        self.syntax_error = syntax_error
        return super().__init__(query_key)
