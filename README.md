# ARCHITECTURE OF THE FLASK APP
 - APP CONTEXT: https://medium.com/hacking-and-slacking/demystifying-flasks-application-context-c7bd31a53817 
 - CONFIGS: https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
 - TEMPLATES: https://realpython.com/flask-blueprint/#including-templates
 - FLASK MIGRATE- https://rest-apis-flask.teclado.com/docs/flask_migrate/add_flask_migrate_to_app/
 - https://levelup.gitconnected.com/remove-pycache-vscode-6c9204399913
 - https://github.com/MGough/flask-microservice-sqlalchemy-marshmallow/blob/master/business/application_factory.py
 - https://medium.com/@jesscsommer/how-to-serialize-and-validate-your-data-with-marshmallow-a815b2276a


## MAIN STEPS

```shell
python3 -m venv vnev
source venv/bin/activate
rm -r migrations
flask --app backend empty-db 
flask db init
flask db migrate
flask db upgrade
flask --app backend seed-db 
```

### VERSION CONTROL
The 'main' branch contains all the main code
The other branches will have code developed in various machines / users
All work done on the various machines will be COMMITted locally. Then 
1. PUSH from local branch to the GitHub remote branch 
2. Create Pull Request: eg. 
   - https://github.com/drguptavivek/backend/pull/new/vivek/mcbook
   - https://github.com/drguptavivek/backend/pull/new/desktop
3. Merge the branch on GitHub with main
4. Checkout the main on local machine


```shell
git clone https://github.com/drguptavivek/backend.git
git checkout main
git remote show origin 
git branch -a
# Create branch for local work
git branch vivek/mcbook
git checkout vivek/mcbook
git add 
git commit  -m "About to Git push a local branch upstream to a remote GitHub repo."
# Push local branch code to remote
git push -u origin vivek/mcbook
# remote: Create a pull request for 'vivek/mcbook' on GitHub by visiting:
# remote:      https://github.com/drguptavivek/backend/pull/new/vivek/mcbook
# merge on GitHub

```

### CONFIGURATIONS
- `config.py`: various configuration sets that can be called when instantiating the Flask app
    - Each configuration set includes parameters. Non-secret configurations can be declared. Secret configs can be loaded from .env
- `.env, .env.production`: various secrets that can be injected in each configuration inside config.py


## ORGANIZATION
1. The app directory containes all application logic
2. myApp/__init__.py includes the factory pattern for creation of Flask app
  - `config_class=DevConfig` means it will load the `DevConfig` configuration from `config.py` which loads secrets from `.env`


## Models inheritance / tree
1. Initialize the SQLAlchemy db object in `myApp/db.py` : `db = SQLAlchemy()`
2. Import and inject db object into the app in `myApp/__init__.py` inside the `create_app` factory :  `from myApp.db import db , db.init_app(app)`
3. Creating Models:
    - Create model in `myApp/models/blueprint_model.py`. 
        - First import the `db` object from `myApp/db.py`
        - Create the Model classes 
    - Import the declared model classes in `myApp/db.py` at the bottom (to avoid circular imports): `from myApp.models import admin_models`


## Migrations
https://flask-migrate.readthedocs.io/en/latest/
1. Import Flask Migrate in `myApp/__init__.py` inside the `create_app` factory
2. Inject the created db and app objects in Migrate db object  `migrate = Migrate(app, db)` 



### Blueprints
1. Create individual Blueprint specific folders inside views oor apis directory. e.g. admin
2. Create __init__.py inside the blueprint specific folder
3. Create a Blueprint_bp.py file inside the blueprint specific folder
4. Instantiate a blueprint object
5. Add Blueprint Views
6. Register the blueprint with its URL prefix in myApp/__init__.py



## Templates:
- https://realpython.com/flask-blueprint/#including-templates


## FLASK_SQLALchemy
https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
https://blog.miguelgrinberg.com/post/what-s-new-in-sqlalchemy-2-0
 - SQLAlchemy 2 In Practice: Learn to program relational databases in Python step by step

For the most part, you should use SQLAlchemy as usual. The SQLAlchemy extension instance creates, configures, and gives access to the following things:
- SQLAlchemy.Model declarative model base class. It sets the table name automatically instead of needing __tablename__.
- SQLAlchemy.session is a session that is scoped to the current Flask application context. It is cleaned up after every request.
- SQLAlchemy.metadata and SQLAlchemy.metadata gives access to each metadata defined in the config.
- SQLAlchemy.engine and SQLAlchemy.engines gives access to each engine defined in the config.
- SQLAlchemy.create_all() creates all tables.
- You must be in an *active Flask application context* to execute queries and to access the session and engine.
 - For convenience, the extension object provides access to names in the sqlalchemy and sqlalchemy.orm modules. 
   - So you can use db.Column instead of importing and using sqlalchemy.Column, although the two are equivalent.
 - 

## SQLALchemy
 - use new Python Type Hinted Mapped_column syntax

### One-to-Many Relationships: example Each department has many units
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many

*Department* : One side   *Unit*: Many Side
 - Add Foreign Key on the Many Side: Unit class
   `department_id: Optional[Mapped[str]] = mapped_column(ForeignKey('departments.id'), index=True)`
 - Add Relationship on the many Side: Unit class - used singular since a unit can have one department
   `department: Mapped['Department'] = relationship(back_populates='units')`3
 - Add Relationship on the One Side: Department class - used plural since a department can have many units 
   `units: Mapped[list['Unit']] = relationship(back_populates='department')`

Explanation
 - Each Unit instance will have a department_id. 
 - Getting a Unit instance will get the related Department instance using the called 'units' relationship
 - Getting a Department will get all the related multiple Unit instances using the called 'department' relationship

### Relationship Loading: lazy vs eager
 - select loader is a lazy loader and is default. The DB query for related object is delayed till that relationship attribute is accessed for the first time
 - joined loader is an eager loader - it accesses all related objects at teh same time as parent is called 
   -  useful if you know you will be accessing related objects
 - Other loaders: raise, raise_on_sql, selectin, write_only, immediate, noload
 - Default loader for a relationship can be changed using the `lazy=` argument
 - For the User Class - joined loader makes sense since it would be good to get the name of the designation as soon as a user is accessed
`designation: Mapped[Designation] = relationship(back_populates='users',  lazy='joined')`
 - For the Designation Class, select loader makes more sense as we may not want to typically get all users of designation

## Cascaded Operations - 
- DETATCH children is parent deleted; Do Not BLOCK Parent deletion if children are present
   - The FKey is ALLOWED  NULLS / Optional
   - cascade = 'save-update, merge'
   - is the DEFAULT behaviour
```
class Department(db.Model):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(str(30), unique=True, index=True)
    units: Mapped[list['Unit']] = relationship(back_populates='department', cascade = 'save-update, merge', lazy='joined')

class Unit(db.Model):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(str(30),  unique=True, index=True)
    department_id: Optional[Mapped[str]] = mapped_column(ForeignKey('departments.id'), index=True)
    department: Mapped['Department'] = relationship(back_populates='units', lazy='joined')
```

- DELETE children is parent deleted; Block parent deletion if children are present
   - The FKey is NOT NULL / NOT Optional
   - cascade = 'all, delete-orphan'
```
class Department(db.Model):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(str(30), unique=True, index=True)
    units: Mapped[list['Unit']] = relationship(back_populates='department', cascade = 'all, delete-orphan', lazy='joined')

class Unit(db.Model):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(str(30),  unique=True, index=True)
    department_id: Mapped[str] = mapped_column(ForeignKey('departments.id'), index=True)
    department: Mapped['Department'] = relationship(back_populates='units', lazy='joined')
```



 - DO not Delete the children if a prent gets deleted. 
This is Optional to allow setting to NULL in case a department gets deleted



   

## Marshmallow
http://marshmallow.readthedocs.io/
## Flask-marshmallow
https://flask-marshmallow.readthedocs.io/en/latest/
Flask-Marshmallow is a thin integration layer for Flask (a Python web framework) and marshmallow (an object serialization/deserialization library) that  
 - adds additional features to marshmallow, 
 - including URL and Hyperlinks fields for HATEOAS-ready APIs. 
 - It also (optionally) integrates with Flask-SQLAlchemy.
 - Generate marshmallow Schemas from your models using `SQLAlchemySchema` or `SQLAlchemyAutoSchema`.
 - SQLAlchemySchema is nearly identical in API to marshmallow_sqlalchemy.SQLAlchemySchema with the following exceptions:
   - By default, SQLAlchemySchema uses the scoped session created by Flask-SQLAlchemy.
   - SQLAlchemySchema subclasses flask_marshmallow.Schema, so it includes the jsonify method.



## marshmallow-sqlalchemy - DO NOT USE AS FLASK MARSHMALLOW ALREADY INCLUDES SQLALCHEMY INTEGRATION
https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
Make sure to declare Models before instantiating Schemas. Otherwise sqlalchemy.orm.configure_mappers() will run too soon and fail.