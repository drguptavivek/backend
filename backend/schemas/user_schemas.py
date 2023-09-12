from marshmallow import fields
from backend.extensions import ma
from backend.models.user_model import Department


class CadreSchema(ma.Schema):
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        Model = Department
        include_fk = True
        include_relationships = True
        load_instance = True
    id = ma.auto_field()



