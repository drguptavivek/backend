# ARCHITECTURE OF THE FLASK APP


## MAIN STEPS
- REQUIRES PYTHON 3.11 FOR THE ` | None` inside  `mobile2: Mapped[int | None] = mapped_column(String(30))` in SQLAlchemy Models.
- Use `virtualenv` to manage python versions. macOS for example comes with 3.9 and one can install version 3.11 in a parallel location by downloading installer from python.org

```shell
git clone https://github.com/drguptavivek/backend.git
cd backend

python3 -m venv vnev
 
# ALTERNATIVE
pip install --user virtualenv
virtualenv venv
virtualenv -p /usr/bin/python3  venv 
# Python 3.9.6

# Install Python 3.11 from https://www.python.org
virtualenv -p /usr/local/bin/python3 venv  
virtualenv -p  /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11    venv
```

```shell
source venv/bin/activate
pip install -r requirements.txt

rm -r migrations
flask --app backend empty-db 
flask db init
flask db migrate
flask db upgrade
flask --app backend seed-db 
```

### VERSION CONTROL
1. The 'main' branch contains all the main code - `git clone https://github.com/drguptavivek/backend.git; git checkout main`
2. Create branches for development locally  `git branch vivek_macbook; git checkout vivek_macbook`
3. All work done on the various machines will be COMMITTED locally `git add; git commit `.  
4. Once work is completed -PUSH from local branch to the GitHub remote / upstream  branch `git push -u origin vivek_macbook` 
5. Got to GitHub website and create a  PULL REQUEST (merge request): e.g. 
   - https://github.com/drguptavivek/backend/pull/new/vivek_macbook
   - https://github.com/drguptavivek/backend/pull/new/desktop
6. Merge the branch on GitHub website with `main` branch
7. Checkout the `main` on local machine ``git remote show origin ; git checkout main ``
   - Now the `main` on local desktop/laptop would be behind the server main
8. Pull the changes from `main` on server to `main` on local - `git pull `


```shell
git clone https://github.com/drguptavivek/backend.git
git checkout main
git remote show origin 
git branch -a

# Create branch for local work
git branch vivek_macbook
git checkout vivek_macbook
git add 
git commit  -m "About to Git push a local branch upstream to a remote GitHub repo."
# Push local branch code to remote
git push -u origin vivek_macbook
# remote: Create a pull request for 'vivek_macbook' on GitHub by visiting:
# remote:      https://github.com/drguptavivek/backend/pull/new/vivek_macbook
# merge on GitHub; Delete remote  vivek_macbook on GitHub

# Back on Laptop
git remote show origin
git checkout main
git pull
git branch --d vivek_macbook
git push origin --delete vivek_macbook
git branch vivek_macbook
git checkout vivek_macbook
git branch -a
git add 
git commit  -m "About to Git push a local branch upstream to a remote GitHub repo."
# Push local branch code to remote
git push -u origin vivek_macbook
# merge on GitHub; Delete remote  vivek_macbook on GitHub



# Back on Desktop
git remote show origin
git checkout main
git pull
git branch --d vivek_desktop # Detach / delete preexisting local branch vivek_desktop
git push origin --delete vivek_desktop # Detach / delete preexisting REMOTE branch vivek_desktop

git branch vivek_desktop
git checkout vivek_desktop
git branch -a
git add 
git commit  -m "About to Git push a local branch vivek_desktop upstream to a remote GitHub repo at vivek_desktop."
# Push local branch code to remote
git push -u origin vivek_desktop 
# merge vivek_desktop with main on GitHub; Delete remote  vivek_desktop on GitHub

```

### CONFIGURATIONS
- `config.py`: various configuration sets that can be called when instantiating the Flask app
    - Each configuration set includes parameters. Non-secret configurations can be declared. Secret configs can be loaded from .env
- `.env, .env.production`: various secrets that can be injected in each configuration inside config.py

## ORGANIZATION
1. The backend directory contains all application logic
2. __init__.py includes the factory pattern for creation of Flask app
  - `config_class=DevConfig` means it will load the `DevConfig` configuration from `config.py` which loads secrets from `.env`

## Models inheritance / tree
1. Initialize the SQLAlchemy db objects and other extensions such as Migrate, Marshmallow etc. in `extensions.py` : `db = SQLAlchemy()`
2. Import extension objects in `__init__.py` inside the `create_app` factory, 
3. Inject the initialized Extension objects in the app inside `app.app_context`
4. Models:
    - Create model in `backend/models/xxx_model.py`. 
        - Import the `db` object from `myApp/db.py`
        - Create the Model classes using the SQLAlchemy 2.0 Declarative Syntax using Type Hints 
    - Import the declared model classes in `models_import.py` : `from backend.models.user_model import Department,....`
    - The models_import.py has already been made available inside the `app.app_context` in `__init__.py`. This allows Flask-Migrate to get all models and run migrations on them  
5. Seeding: The db_initializer folder contains an  `db_initializer.py`
   - `db.engine.url.database` - is used to get the current database name
   - Functions such as `create_department(), create_faculty_cadre(), create_user()` have been created. Each function 
     - Truncates the tables affected by that class - Table name is manually being set inside function. Foreign Key checks arr disabled and re-enabled
     - Creates the objects of Model . Example - Department model class `department = Department(...)`
     - Adds data for various named properties of the Model class
     - Leverages relationships to add child objets using the related child Model properties: eg   `department = Department(... departmentUnits=[Unit(...), Unit(...),Unit(...)])`
   - `click` is used to add commandline functions to EMPTY-DB and SEED-DB.  `@click.command('seed-db')     def seed_db_command():`
   - `Click` Functions once declared in `db_initializer.py` are registered with the main __init__.py inside application context - `app.cli.add_command(seed_db_command)`

## Migrations
https://flask-migrate.readthedocs.io/en/latest/
1. Import and instantiate Flask Migrate in `extensions.py` 
2. Inject the created db and app objects in Migrate db object  `migrate = Migrate(app, db)`   inside the `create_app` factory in `app.app_context`





## SQLAlchemy
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
 - Other loaders: `raise, raise_on_sql, selectin, write_only, immediate, noload`
 - Default loader for a relationship can be changed using the `lazy=` argument
 - For the User Class 
    -  joined loader makes sense since it would be good to get the name of the designation as soon as a user is accessed
        `designation: Mapped[Designation] = relationship(back_populates='users',  lazy='joined')`
   - *HOWEVER, joined loader causes problems with SELECT statements necessitating the need of UNIQUE() otherwise multiple related rows are fetched*
 - For the Designation Class, select loader makes more sense as we may not want to typically get all users of designation

### Cascaded Operations - 
- DETACH children is parent deleted; Do Not BLOCK Parent deletion if children are present
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


## Marshmallow Schemas
Declare schemas in 'schemas' folder



## Blueprints - TODO
1. Create individual Blueprint specific folders inside views oor apis directory. e.g. admin
2. Create __init__.py inside the blueprint specific folder
3. Create a Blueprint_bp.py file inside the blueprint specific folder
4. Instantiate a blueprint object
5. Add Blueprint Views
6. Register the blueprint with its URL prefix in myApp/__init__.py



## Templates: - TODO
- https://realpython.com/flask-blueprint/#including-templates
