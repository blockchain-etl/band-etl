import base64
import json


def base64_string_to_bytes(val):
    if val is None:
        return None
    return base64.b64decode(val)


def bytes_to_base64_string(val):
    if val is None:
        return None
    return base64.b64encode(val).decode('utf-8')


def to_int(val):
    if val is None:
        return val
    if isinstance(val, str):
        return int(val)

    return val


def json_dumps(obj):
    if obj is None:
        return None
    return json.dumps(obj, separators=(',', ':'), cls=CustomEncoder)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return bytes_to_base64_string(obj)
        return json.JSONEncoder.default(self, obj)
