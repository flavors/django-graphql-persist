from django.template.utils import get_app_template_dirs

from ..settings import persist_settings
from .filesystem import FilesystemLoader


class AppDirectoriesLoader(FilesystemLoader):

    def get_dirs(self):
        return get_app_template_dirs(persist_settings.APP_DOCUMENT_DIR)
