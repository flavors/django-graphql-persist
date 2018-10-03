import json
from collections import OrderedDict

from django.utils.encoding import force_text


def parse_json(content, **kwargs):
    content = force_text(content, **kwargs)
    return json.loads(content, object_pairs_hook=OrderedDict)


def parse_body(request):
    if request.content_type == 'application/json':
        try:
            return parse_json(request.body)
        except ValueError:
            return None

    elif request.content_type in (
            'application/x-www-form-urlencoded',
            'multipart/form-data'):

        return request.POST.dict()
    return None
