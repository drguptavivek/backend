
 - APP CONTEXT: https://medium.com/hacking-and-slacking/demystifying-flasks-application-context-c7bd31a53817 
 - CONFIGS: https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
 - TEMPLATES: https://realpython.com/flask-blueprint/#including-templates
 - FLASK MIGRATE- https://rest-apis-flask.teclado.com/docs/flask_migrate/add_flask_migrate_to_app/
 - https://levelup.gitconnected.com/remove-pycache-vscode-6c9204399913
 - https://github.com/MGough/flask-microservice-sqlalchemy-marshmallow/blob/master/business/application_factory.py
 - https://medium.com/@jesscsommer/how-to-serialize-and-validate-your-data-with-marshmallow-a815b2276a



### 
- https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation
mapped_column() derives the datatype and nullability from the Mapped annotation
The two qualities that mapped_column() derives from the Mapped annotation are:
- datatyppe - Python type given in Mapped Class
```python
class Account(db.Model):
    __tablename__ = "accounts"
    col1  = Mapped[bool] = mapped_column(Boolean)
    col2  = Mapped[bytes] = mapped_column(LargeBinary)
    col3  = Mapped[date] = mapped_column(Date)
    col4  = Mapped[datetime] = mapped_column(DateTime)
    col5  = Mapped[time] = mapped_column(Time)
    col6  = Mapped[timedelta] = mapped_column(Interval)
    col7  = Mapped[Decimal] = mapped_column(Numeric)
    col8  = Mapped[float] = mapped_column(Float)
    col9  = Mapped[int] = mapped_column(Integer)
    col10 = Mapped[str] = mapped_column(String(10))
    col11 = Mapped[str] = mapped_column(String(20))
    col12 =  Mapped[uuid.UUID] = mapped_column(Uuid())

https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types

```
https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Uuid
SQLAlchemy types `Uuid` Represent a database agnostic UUID datatype.
In its default mode of use, the Uuid datatype expects Python `uuid` objects, from the Python `uuid` module:

SQLAlchemy types `UUID` Represent the SQL UUID type. The UUID datatype only works on databases that have a SQL datatype 
named UUID. It will not function for backends which don’t have this exact-named type, including SQL Server. 
For backend-agnostic UUID values with native support, including for SQL Server’s UNIQUEIDENTIFIER datatype, use the Uuid datatype.

- nullability - The mapped_column.nullable parameter, when present, will always take precedence:

```python
   # primary_key=True, therefore will be NOT NULL
    id: Mapped[int] = mapped_column(primary_key=True)

    # not Optional[], therefore will be NOT NULL
    data: Mapped[str]

    # Optional[], therefore will be NULL
    additional_info: Mapped[Optional[str]]
    
    # will be String() NOT NULL, but can be None in Python
    data: Mapped[Optional[str]] = mapped_column(nullable=False)
    
    # will be String() NULL, but type checker will not expect
    # the attribute to be None
    data: Mapped[str] = mapped_column(nullable=True)

```

### Enums
https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-python-enum-or-pep-586-literal-types-in-the-type-map
```python
import enum
from typing import Literal
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"

class SomeClass(Base):
    __tablename__ = "some_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status]



Status2 = Literal["pending", "received", "completed"]

class SomeClass2(Base):
    __tablename__ = "some_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status2]

```
 



## FLASK_SQLAlchemy
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
https://blog.miguelgrinberg.com/post/what-s-new-in-sqlalchemy-2-0

BOOK - SQLAlchemy 2 In Practice: Learn to program relational databases in Python step by step
https://www.amazon.in/SQLAlchemy-Practice-program-relational-databases-ebook/dp/B0BVJRKS54


For the most part, you should use SQLAlchemy as usual. The SQLAlchemy extension instance creates, configures, and gives access to the following things:
- `SQLAlchemy.Model` declarative model base class. It sets the table name automatically instead of needing `__tablename__`.
- `SQLAlchemy.session` is a session that is scoped to the current Flask application context. It is cleaned up after every request.
- `SQLAlchemy.metadata` and `SQLAlchemy.metadata` gives access to each metadata defined in the config.
- `SQLAlchemy.engine` and `SQLAlchemy.engines` gives access to each engine defined in the config.
- `SQLAlchemy.create_all()` creates all tables.
- You must be in an *active Flask application context* to execute queries and to access the session and engine.
 - For convenience, the extension object provides access to names in the sqlalchemy and sqlalchemy.orm modules. 
   - So you can use db.Column instead of importing and using sqlalchemy.Column, although the two are equivalent.
 - 

  

## Marshmallow
http://marshmallow.readthedocs.io/
https://marshmallow.readthedocs.io/en/stable/examples.html

Serializing Objects  = Dumping - Python Objects to JSON
Deserializing Objects  = Loading - JSON to DICT which can be used to create Objects



In the context of a web API:
- dump_only  = read-only fields - example created_at field wil not be included in POST Request
- load_only  = write-only” field - example password fiedl will not be output in a GET request

Two-way Nesting - If two schemas nest each other, exclude related fields or restrict related field (esclude the nested of nested field)
```python
class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    # Make sure to use the 'only' or 'exclude' to avoid infinite recursion
    author = fields.Nested(lambda: AuthorSchema(only=("id", "title")))

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    books = fields.List(fields.Nested(BookSchema(exclude=("author",))))

class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    # Use the 'exclude' argument to avoid infinite recursion
    employer = fields.Nested(lambda: UserSchema(exclude=("employer",)))
    friends = fields.List(fields.Nested(lambda: UserSchema()))
```

### Schema Meta Options - Marshmallow
Meta = Options object for a Schema. Options in plain Marshmallow - https://marshmallow.readthedocs.io/en/latest/marshmallow.schema.html#marshmallow.schema.Schema.Meta
 - fields: Tuple or list of fields to include in the serialized result. fields = ("id", "email", "date_created")
 - additional: Tuple or list of fields to include in addition to the  explicitly declared fields. additional and fields are mutually-exclusive options. 
 - include: Dictionary of additional fields to include in the schema.
 - exclude: Tuple or list of fields to exclude in the serialized result exclude = ("password", "secret_attribute")
 - dateformat: Default format for Date fields.
 - datetimeformat: Default format for DateTime fields.
 - load_only: Tuple or list of fields to exclude from serialized results.
 - dump_only: Tuple or list of fields to exclude from deserialization
 - unknown: Whether to exclude, include, or raise an error for unknown


### marshmallow-sqlalchemy
https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
Make sure to declare Models before instantiating Schemas. Otherwise, sqlalchemy.orm.configure_mappers() will run too soon and fail.

Provides
-  SQLAlchemySchema: has following META options 
   - model: The SQLAlchemy model to generate the Schema from (mutually exclusive with table).
   - load_instance: Whether to load model instances.
- SQLAlchemyAutoSchema: : has following META options
  - include_fk: Whether to include foreign fields; defaults to False.
  - include_relationships: Whether to include relationships; defaults to False.
  - Any field generated by a SQLAlchemyAutoSchema can be overridden https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#overriding-generated-fields
- auto_field() - autodetect field type from Model
https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#base-schema-i


### Flask-marshmallow
https://flask-marshmallow.readthedocs.io/en/latest/
Flask-Marshmallow is a thin integration layer for Flask (a Python web framework) and marshmallow (an object serialization/deserialization library) that
 - including URL and Hyperlinks fields for HATEOAS-ready APIs. 
 - It also (optionally) integrates with Flask-SQLAlchemy.
 - Generate marshmallow Schemas from your models using `SQLAlchemySchema` or `SQLAlchemyAutoSchema`.
 - SQLAlchemySchema is nearly identical in API to marshmallow_sqlalchemy.SQLAlchemySchema with the following exceptions:
   - By default, SQLAlchemySchema uses the scoped session created by Flask-SQLAlchemy.
   - SQLAlchemySchema subclasses flask_marshmallow.Schema, so it includes the jsonify method.


#### Fields in Marshmallow
https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#module-marshmallow.fields

String(*, load_default, missing, ...) A string field.
Integer(*[, strict])    An integer field.
Float(*[, allow_nan, as_string])    A double as an IEEE-754 double precision string.
Decimal([places, rounding, allow_nan, as_string]) A field that (de)serializes to the Python decimal.Decimal type.
Date([format]) ISO8601-formatted date string.
DateTime([format])  A formatted datetime string.
Boolean(*[, truthy, falsy]) A boolean field.
Email(*args, **kwargs)  An email field.
Time([format]) A formatted time string. 
TimeDelta(precision, serialization_type, ...) A field that (de)serializes a datetime.timedelta object to an integer or float and vice versa.
UUID(*, load_default, missing, dump_default, ...)    A UUID field.
Url(*[, relative, absolute, schemes, ...])   An URL field.

Enum(enum, *[, by_value])   An Enum field (de)serializing enum members by symbol (name) or by value.
List(cls_or_instance, **kwargs) A list field, composed with another Field class or instance.
Dict([keys, values]) A dict field.
Tuple(tuple_fields, *args, **kwargs) A tuple field, composed of a fixed number of other Field classes or instances

Nested(nested, ...) Allows you to nest a Schema inside a field.

Method([serialize, deserialize]) A field that takes the value returned by a Schema method.
Mapping([keys, values]) An abstract class for objects with key-value pairs.
Function([serialize, deserialize])  A field that takes the value returned by a function.

Field(*, load_default, missing, ...)    Basic field from which other fields should extend.
Number(*[, as_string]) Base class for number fields.

IP(*args[, exploded])   A IP address field.
IPv4(*args[, exploded]) A IPv4 address field.
IPv6(*args[, exploded]) A IPv6 address field.
NaiveDateTime([format, timezone]) A formatted naive datetime string.
Pluck(nested, field_name, **kwargs) Allows you to replace nested data with one of the data's fields.
Raw(*, load_default, missing, dump_default, ...) Field that applies no formatting.


###  Validations in Marshmallow
Validation occurs on deserialization (LOAD, JSON TO OBEJECT) but not on serialization. To improve serialization performance, data passed to Schema.dump() are considered valid.
https://www.golinuxcloud.com/python-marshmallow/
 - required 
 - validate: https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#api-validators
   - validate.Length
   - validate.Range
   - validate.OneOf, validate.NoneOf 
   - validate.ContainsOnly, ContainsNoneOf - for sequences
   - validate.Email
   - validate.Equal
   - validate.URL
   - validate.Regexp 
   - validate.Validator - custom defined validator: validate.And(validate.Range(min=0), validate.Length(max=00), custom_validator_function)
   - validate.And ; combine multiple valdiations
  - validates -  for cross field validation
  - validates_schema
   - 

```python
from marshmallow import Schema, fields, validate, validates, ValidationError, ValidationError

# CUSTOM validator FUNCTION
def validate_quantity(n):
    if n < 0:
        raise ValidationError("Quantity must be greater than 0.")
    if n > 30:
        raise ValidationError("Quantity must not be greater than 30.")

 # STANDARD VALIDATOR METHODS AND USE OF VALIDATOR FUCNTION   
class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))
    age2 = fields.Integer(required=True, error_messages={"required": "Age is required."})
    city = fields.String(
        required=True,
        error_messages={"required": {"message": "City required", "code": 400}},
    )
    email = fields.Email()
    quantity = fields.Integer(validate=validate_quantity)

# Field Validators as Methods
class ItemSchema(Schema):
    quantity = fields.Integer()

    @validates("quantity")
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity must be greater than 0.")
        if value > 30:
            raise ValidationError("Quantity must not be greater than 30.")

from marshmallow import Schema, fields, validates_schema, ValidationError

 # SCHEMA LEVEL VALDIATION - COMPARE ONE FIEDL AGAINST ANOTHER 
class NumberSchema(Schema):
    field_a = fields.Integer()
    field_b = fields.Integer()

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["field_b"] >= data["field_a"]:
            raise ValidationError("field_a must be greater than field_b")


schema = NumberSchema()
try:
    schema.load({"field_a": 1, "field_b": 2})
except ValidationError as err:
    err.messages["_schema"]
# => ["field_a must be greater than field_b"]        
        
        
 # DEFAULT VALUES
class UserSchema2(Schema):
    id = fields.UUID(load_default=uuid.uuid1)
    birthdate = fields.DateTime(dump_default=dt.datetime(2017, 9, 29))
UserSchema2().load({})
# {'id': UUID('337d946c-32cd-11e8-b475-0022192ed31b')}
UserSchema2().dump({})
# {'birthdate': '2017-09-29T00:00:00+00:00'}


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema2)


```


