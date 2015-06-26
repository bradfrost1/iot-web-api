import json as _json
import datetime


class JSONEncoder(_json.JSONEncoder):
    allow_nan = False
    sort_keys = False

    def default(self, obj):
        if (isinstance(obj, datetime.datetime) or
            isinstance(obj, datetime.date) or
            isinstance(obj, datetime.time)
        ):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return _json.JSONEncoder.default(self, obj)


class JSONDecoder(_json.JSONDecoder):
    strict = True
