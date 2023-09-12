import logging
from pprint import pp
import click
from sqlalchemy.sql import text

from backend.extensions import db
from backend.models.user_model import Account, Department, Cadre, Designation, Unit, User
from config import ProdConfig
# https://github.com/melihcolpan/flask-restful-login/blob/master/api/db_initializer/db_initializer.py
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist



@click.command('init-db')
def init_db_command():
    """Seed the tables."""
    from backend.db_initializer.db_initializer import create_department
    create_department()
    from backend.db_initializer.db_initializer import create_faculty_cadre
    create_faculty_cadre()
    create_user()
    click.echo('Seeded the database.')


def create_department():
    database = db.engine.url.database #    pp (database)
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database +'.departments')
    stmt3 = text('TRUNCATE TABLE ' + database +'.units')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt3)
    db.session.execute(stmt4)

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
        logging.info("Department RPC was Added.")

    else:
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
        logging.info("Department Anaesthesiology was Added.")

    else:
        logging.info("department Anaesthesiology already set.")


def create_faculty_cadre():
    database = db.engine.url.database #    pp (database)
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database +'.cadres')
    stmt3 = text('TRUNCATE TABLE ' + database +'.designations')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    db.session.execute(stmt3)
    db.session.execute(stmt4)
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





def create_user():
    database = db.engine.url.database #    pp (database)
    stmt1 = text('SET FOREIGN_KEY_CHECKS=0')
    stmt2 = text('TRUNCATE TABLE ' + database +'.users')
    #stmt3 = text('TRUNCATE TABLE ' + database +'.designations')
    stmt4 = text('SET FOREIGN_KEY_CHECKS=1')
    db.session.execute(stmt1)
    db.session.execute(stmt2)
    #db.session.execute(stmt3)
    db.session.execute(stmt4)
    user = User.query.filter_by(email="vivekgupta@aiims.gov.in").first()
    if user is None:
        user = User(
            fullname="Dr Vivek Gupta",
            employee_id="E100056",
            email="vivekgupta@aiims.gov.in",
            mobile="9899410420",
            department_id = "1",
            designation_id = "3",
            inactive = "0",
        )
        db.session.add(user)
        db.session.commit()
        logging.info(f"User Vivek Gupta Added.")

    else:
        logging.info(f"User Vivek Gupta already set.")






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