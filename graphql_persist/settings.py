from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed

DEFAULTS = {
    'DOCUMENTS_DIRS': (),
    'DOCUMENTS_EXT': '.graphql',
    'CACHE_NAME': 'default',
    'QUERY_KEY_HANDLER': 'graphql_persist.query.query_key_handler',
    'DEFAULT_VERSIONING_CLASS': None,
    'DEFAULT_LOADER_ENGINE_CLASS': 'graphql_persist.loaders.Engine',
    'DEFAULT_LOADER_CLASSES': (
        'graphql_persist.loaders.AppDirectoriesLoader',
        'graphql_persist.loaders.FilesystemLoader',
        'graphql_persist.loaders.URLLoader',
    ),
    'DEFAULT_RENDERER_CLASSES': (),

    # Versioning
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',
    'MEDIA_TYPE_NAME': r'[a-z0-9]+',

    # Loaders
    'APP_DOCUMENT_DIR': 'documents',
}

IMPORT_STRINGS = (
    'QUERY_KEY_HANDLER',
    'DEFAULT_VERSIONING_CLASS',
    'DEFAULT_LOADER_ENGINE_CLASS',
    'DEFAULT_LOADER_CLASSES',
    'DEFAULT_RENDERER_CLASSES',
)


def perform_import(value, setting_name):
    if value is None:
        return None
    if isinstance(value, str):
        return import_from_string(value, setting_name)
    elif isinstance(value, (list, tuple)):
        return [import_from_string(item, setting_name) for item in value]
    return value


def import_from_string(value, setting_name):
    try:
        module_path, class_name = value.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = 'Could not import `{}` for Persist setting `{}`. {}: {}.'.format(
            value, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class PersistSettings:

    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid setting: `{}`'.format(attr))

        value = self.user_settings.get(attr, self.defaults[attr])

        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRAPHQL_PERSIST', {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']

    if setting == 'GRAPHQL_PERSIST':
        persist_settings.reload()


setting_changed.connect(reload_settings)

persist_settings = PersistSettings(DEFAULTS, IMPORT_STRINGS)
