from init import db, ma
from marshmallow import fields


def camel_case(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCasedSchema(ma.Schema):
    def on_bind_field(self, field_name, field_object):
        field_object.data_key = camel_case(field_object.data_key or field_name)
