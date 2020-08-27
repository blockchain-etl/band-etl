import json


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