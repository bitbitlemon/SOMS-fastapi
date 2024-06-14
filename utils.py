from datetime import datetime
from sqlalchemy.orm import class_mapper


def object_to_dict(obj) -> dict:
    if obj:
        columns = [column.key for column in class_mapper(obj.__class__).columns]
        get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
        return dict(map(get_key_value, columns))
    return {}


class ProjectException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
