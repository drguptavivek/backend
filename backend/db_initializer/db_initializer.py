import logging
from backend.extensions import db
from backend.models.user_model import Department, Cadre, Designation, Unit
# https://github.com/melihcolpan/flask-restful-login/blob/master/api/db_initializer/db_initializer.py
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist


def create_department():
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
        logging.info(f"{cadre}  Added.")

    else:
        logging.info(f"cadre {cadre} already set.")




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