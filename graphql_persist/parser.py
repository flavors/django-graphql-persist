import json
from collections import OrderedDict

from django.utils.encoding import force_text


def parse_json(content, **kwargs):
    content = force_text(content, **kwargs)
    return json.loads(content, object_pairs_hook=OrderedDict)
