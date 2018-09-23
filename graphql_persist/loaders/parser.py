import re
from functools import partial

from graphql.language import ast
from graphql.language.printer import print_ast

from .exceptions import DocumentDoesNotExist, DocumentImportError

__all__ = ['parse_document']


import_regex = re.compile(r'#\s+from\s+(.*)\s+import\s+(.*)')


def fragments_generator(value, definitions):
    if getattr(value, 'selection_set', None) is not None:
        for selection in value.selection_set.selections:
            yield from fragments_generator(selection, definitions)

    elif isinstance(value, ast.FragmentSpread):
        if value.name.value in definitions:
            fragment = definitions[value.name.value]
            yield fragment
            yield from fragments_generator(fragment, definitions)


def parse_definitions(identifiers, definitions):
    ret = ''
    fragments = set()

    for identifier in identifiers.split(','):
        identifier = identifier.strip()

        if identifier not in definitions:
            msg = 'Cannot import definition `{}`'.format(identifier)
            raise DocumentImportError(msg)

        definition = definitions[identifier]
        ret += print_ast(definition)
        fragments.update(fragments_generator(definition, definitions))

    return ''.join(print_ast(fragment) for fragment in fragments) + ret


def import_definitions(origin, match):
    name, identifiers = match.groups()
    path = name.lstrip('.')
    dots = len(name) - len(path)
    query_key = origin.query_key[:-dots] + path.split('.')

    try:
        imported = origin.loader.engine.get_document(query_key)
    except DocumentDoesNotExist:
        msg = 'No document named `{}`'.format(query_key)
        raise DocumentImportError(msg)

    return parse_definitions(identifiers, imported.definitions)


def parse_document(document):
    header = document.source.body[:document.ast.loc.start]
    origin = document.origin
    source = import_regex.sub(partial(import_definitions, origin), header)
    return source + document.source.body[document.ast.loc.start:]
