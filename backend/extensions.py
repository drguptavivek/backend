from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase


# Create db object. This db object will be imported in various model definitions
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()



def print_rows(x):
    for row in x:
        print(row)


# Import various models that have inherited the db object and have defined the tables, field, relationships etc
