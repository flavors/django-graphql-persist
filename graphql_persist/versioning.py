import re

from django.http.multipartparser import parse_header
from django.utils.translation import ugettext_lazy as _

from . import exceptions
from .settings import persist_settings


class BaseVersioning:
    default_version = persist_settings.DEFAULT_VERSION
    allowed_versions = persist_settings.ALLOWED_VERSIONS

    def get_version(self, request):
        raise NotImplementedError('.get_version() must be implemented')

    def is_allowed_version(self, version):
        if not self.allowed_versions:
            return True
        return (version == self.default_version or
                version in self.allowed_versions)


class AcceptHeaderVersioning(BaseVersioning):
    version_param = persist_settings.VERSION_PARAM

    def parse_header(self, media_type):
        base_media_type, params = parse_header(media_type)
        return params.get(self.version_param, self.default_version)

    def get_version(self, request):
        media_type = request.META.get('HTTP_ACCEPT', '').encode('utf-8')
        version = self.parse_header(media_type)

        if hasattr(version, 'decode'):
            version = version.decode('iso-8859-1')

        if not self.is_allowed_version(version):
            raise exceptions.GraphQLPersistError(
                _('Invalid version in "Accept" header'))
        return version


class VendorTreeVersioning(AcceptHeaderVersioning):
    media_type_regex = re.compile(
        r'^application/vnd\.{}\.([a-z0-9\.]+[a-z0-9]+)\+json$'
        .format(persist_settings.MEDIA_TYPE_NAME).encode(),
        re.IGNORECASE)

    def parse_header(self, media_type):
        match = self.media_type_regex.match(media_type)

        if not match:
            return self.default_version
        return match.group(1)


class QueryParameterVersioning(BaseVersioning):
    version_param = persist_settings.VERSION_PARAM

    def get_version(self, request):
        version = request.GET.get(self.version_param, self.default_version)

        if not self.is_allowed_version(version):
            raise exceptions.GraphQLPersistError(
                _('Invalid version in query parameter'))
        return version


class HostNameVersioning(BaseVersioning):
    hostname_regex = re.compile(
        r'^([a-z0-9]+)\.[a-z0-9]+\.[a-z0-9]+$',
        re.IGNORECASE)

    def get_version(self, request):
        hostname, separator, port = request.get_host().partition(':')
        match = self.hostname_regex.match(hostname)

        if not match:
            return self.default_version

        version = match.group(1)

        if not self.is_allowed_version(version):
            raise exceptions.GraphQLPersistError(
                _('Invalid version in hostname'))
        return version
