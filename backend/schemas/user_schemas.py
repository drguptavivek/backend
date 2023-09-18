from marshmallow import fields, validate, validates
from backend.extensions import ma, db
from backend.models.user_model import Department, Account, Role, AccountRole, Cadre


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        Model = Account
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=10))
    uid = fields.UUID(dump_only=True)
    password = fields.String(load_only=True, validate=validate.Length(min=8))
    created_by = fields.String(required=True)
    create_date = fields.DateTime(dump_only=True)
    inactive = fields.Integer()
    inactive_date = fields.DateTime(dump_only=True)
    inactive_by = fields.Integer()
    AccountHasRoles = fields.Nested(lambda: RoleSchema(only=("id", "name")))


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        Model = Role
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=20))


class AccountRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Model = AccountRole
        include_fk = True
        include_relationships = True
        load_instance = True
        sqla_session = db.session
    account_id = ma.auto_field()
    role_id = ma.auto_field()


class CadreSchema(ma.SQLAlchemySchema):
    class Meta:
        Model = Cadre
        include_fk = True
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        Model = Department
        include_fk = True
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    



