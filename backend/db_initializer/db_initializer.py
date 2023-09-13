import logging
from pprint import pp
import click
from sqlalchemy.sql import text, select

from backend.extensions import db, print_rows
from backend.models.user_model import Account, Department, Cadre, Designation, Unit, User

# https://github.com/melihcolpan/flask-restful-login/blob/master/api/db_initializer/db_initializer.py
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist




@click.command('empty-db')
def empty_db_command():
    """Seed the tables."""
    drop_database()
    click.echo('Deleted and Recreated the empty database. '
               'Run --- '
               'flask db init, '
               'flask db migrate, '
               'flask db upgrade')


@click.command('seed-db')
def seed_db_command():
    """Seed the tables."""
    create_department()
    create_faculty_cadre()
    create_user()
    click.echo('Seeded the database.')


def drop_database():
    database=db.engine.url.database
    pp(database)
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('DROP DATABASE ' + database)
    stmt3 = text('CREATE DATABASE ' + database)
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt3)
    db.session.execute(stmt4)


def create_department():
    database = db.engine.url.database

    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database + '.departments')
    stmt3 = text('TRUNCATE TABLE ' + database + '.units')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt3)
    db.session.execute(stmt4)
    print(f'Truncated {database}.departments and {database}.units')
    department = Department.query.filter_by(abbr="RPC").first()
    if department is None:
        department = Department(
            name="Dr RP Center for Ophthalmic Sciences",
            abbr="RPC",
            type="CENTER",
            departmentUnits=[
                Unit(name="RPC Unit 1", abbr="U-1"),
                Unit(name="RPC Unit 2", abbr="U-2"),
                Unit(name="RPC Unit 3", abbr="U-3"),
                Unit(name="RPC Unit 4", abbr="U-4"),
                Unit(name="RPC Unit 5", abbr="U-5"),
                Unit(name="RPC Unit 6", abbr="U-6"),
                Unit(name="Ocular Anesthesia", abbr="Ocu Anes"),
            ]
        )
        db.session.add(department)
        db.session.commit()
        print("Department RPC was Added with 6 units and Ocular anaesthesia.")
        logging.info("Department RPC was Added.")

    else:
        print("department RPC already set.")
        logging.info("department RPC already set.")

    department = Department.query.filter_by(abbr="Anaes").first()
    if department is None:
        department = Department(
            name="Anaesthesiology",
            abbr="Anaes",
            type="Department",
        )
        db.session.add(department)
        db.session.commit()
        print("Department Anaesthesiology was Added.")
        logging.info("Department Anaesthesiology was Added.")

    else:
        print("department Anaesthesiology already set.")
        logging.info("department Anaesthesiology already set.")

    query = select(Department)
    # print(f'{query}')
    departments = db.session.execute(query).all()
    print('ALL DEPARTMENTS')
    print_rows(departments)

    query = select(Unit)
    # print(f'{query}')
    units = db.session.execute(query).all()
    print(f'All Units : ')
    print_rows(units)

def create_faculty_cadre():
    database = db.engine.url.database  # pp (database)
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database + '.cadres')
    stmt3 = text('TRUNCATE TABLE ' + database + '.designations')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt3)
    db.session.execute(stmt4)
    print(f'Truncated {database}.cadres and {database}.designations')

    cadre = Cadre.query.filter_by(name="Faculty").first()
    if cadre is None:
        cadre = Cadre(
            name="Faculty",
            cadreDesignations=[
                Designation(name="Assistant Professor", abbr="Asst Prof"),
                Designation(name="Associate Professor", abbr="Assoc Prof"),
                Designation(name="Additional Professor", abbr="Addl Prof"),
                Designation(name="Professor", abbr="Prof"),
            ],
        )
        db.session.add(cadre)
        db.session.commit()
        logging.info(f"Faculty Cadre and Designations Added.")


    else:
        logging.info(f"Faculty Cadre and Designations already set.")

    query = select(Cadre)
    #print(f'{query}')
    cadres = db.session.execute(query).all()
    print('ALL CADRES')
    print_rows(cadres)

    query = select(Designation)
    #print(f'{query}')
    designations = db.session.execute(query).all()
    print('ALL DESIGNATIONS')
    print_rows(designations)


def create_user():
    database = db.engine.url.database
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database + '.users')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt4)
    print(f'Truncated {database}.users')

    query = select(Cadre.id).where(Cadre.name == "Faculty")
    cadreid = db.session.scalar(query)
    print(f'CADRE ID for faculty = {cadreid}')

    query = select(Designation.id).where(Designation.name == "Additional Professor", Designation.cadre_id== cadreid)
    designationid = db.session.scalar(query)
    print(f'Designation ID for Faculty Cadre Additional Professor  = {designationid}')

    query = select(Department.id).where(Department.name =="Dr RP Center for Ophthalmic Sciences")
    departmentid = db.session.scalar(query)
    print(f'Department_id for Dr RP Center for Ophthalmic Sciences = {departmentid}')

    query = select(User.id).where(User.fullname == "Dr Vivek Gupta", User.employee_id == "E100056")
    existing_user = db.session.execute(query).one_or_none()
    print(f' USERS already in table  = {existing_user}')

    if existing_user is None:
        new_user = User(
            fullname='Dr Vivek Gupta',
            employee_id="XXXXXXXX",
            email="vivekguptaXXXXX@aiims.gov.in",
            mobile="XXXXXXXX",
            department_id=departmentid,
            cadre_id=cadreid,
            designation_id=designationid,
            inactive="0"
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"User Vivek Gupta Added.")
        logging.info(f"User Vivek Gupta Added.")

    else:
        print(f"User Vivek Gupta, Employee ID E100056 already set.")
        logging.info(f"User Vivek Gupta, Employee ID E100056 already set.")

    query = select(User)
    users = db.session.execute(query).all()
    print(f'ALL USERS')
    print_rows(users)





# def create_cadre():
#     cadrelist = ["Faculty", "Residents", "Nursing", "OT Technicians"]
#     for cadres in cadrelist:
#         print(f"{cadres}")
#         cadre = Cadre.query.filter_by(name=cadres).first()
#         if cadre is None:
#             cadre1 = Cadre(name=cadres)
#             db.session.add(cadre1)
#             db.session.commit()
#             logging.info(f"{cadre}  Added.")
#
#         else:
#             logging.info(f"cadre {cadre} already set.")