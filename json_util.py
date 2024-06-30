

from datetime import datetime, date
import json
from dataclasses import is_dataclass, asdict
from decimal import Decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)

        if isinstance(o, (date, datetime)):
            return o.isoformat()

        if isinstance(o, Decimal):
            return str(o)

        return json.JSONEncoder.default(self, o)


def json_dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)


def json_loads(s):
    return json.loads(s)
