from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# Create db object. This db object will be imported in various model definitions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

# Import various models that have inherited the db object and have defined the tables, field, relationships etc
