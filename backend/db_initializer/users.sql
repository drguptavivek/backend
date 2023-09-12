
INSERT INTO departments (name, abbr, type)
VALUES
    ("Dr RP Center for Ophthalmic Sciences", "RPC", "CENTER"),
    ("Anaesthesiology", "Anaes", "Department");

INSERT INTO units (name, abbr, department_id)
VALUES
    ("Unit I", "Unit 1", 1),
    ("Unit II", "Unit 2", 1),
    ("Unit III", "Unit 3", 1),
    ("Unit IV", "Unit 4", 1),
    ("Unit V", "Unit 5", 1),
    ("Unit VI", "Unit VI", 1),
    ("Ocu Anesthesia", "RPC Anes", 1);


INSERT INTO cadres (name)
    VALUES ("Faculty"), ("Residents"), ("Nursing"), ("OT Technicians");



INSERT INTO designations (name, abbr, cadre_id)
VALUES
    ("Assistant Professor", "Asst Prof", 1),
    ("Associate Professor", "Asso Prof", 1),
    ("Additional Professor", "Addl Prof", 1),
    ("Professor", "Prof", 1),
    ("Senior Resident", "SR", 2),
    ("Junior Resident", "JR", 2),
    ("Nursing officer", "Nurse", 3),
    ("Senior Nursing officer", "Sr.Nurse", 3),
    ("Assitant Nursing Suprintendet", "ANS", 3),
    ("Deputy Nursing Suprintendet", "DNS", 3),
    ("OT Technician", "OTA", 4);


INSERT INTO roles (name)
    VALUES ("Consultant"), ("SR"), ("JR"), ("OT Nurse"), ("Ward Nurse");

