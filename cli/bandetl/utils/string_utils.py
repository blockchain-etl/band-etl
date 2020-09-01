import base64
import json


def base64_string_to_bytes(val):
    if val is None:
        return None
    return base64.b64decode(val)


def to_int(val):
    if val is None:
        return val
    if isinstance(val, str):
        return int(val)

    return val


def json_dumps(obj):
    if obj is None:
        return None
    return json.dumps(obj, separators=(',', ':'))
