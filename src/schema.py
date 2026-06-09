import csv
from db import get_connection

def _clean(value):
    """Convert literal CSV strings like 'NULL', '', 'None' into Python None."""
    if value is None:
        return None
    if isinstance(value, str) and value.strip().upper() in ("NULL", "", "NONE"):
        return None
    return value

def create_tables():
    """Executes all the DDL statements to initialize the schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                uid      INT          PRIMARY KEY,
                email    VARCHAR(100) NOT NULL UNIQUE,
                username VARCHAR(100) NOT NULL,
                joined   DATE         NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Organizer (
                uid        INT          PRIMARY KEY,
                department VARCHAR(150) NOT NULL,
                experience INT          NOT NULL,
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Participant (
                uid  INT PRIMARY KEY,
                type VARCHAR(150),
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Administrator (
                uid       INT         PRIMARY KEY,
                firstname VARCHAR(50) NOT NULL,
                lastname  VARCHAR(50) NOT NULL,
                FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Event (
                eid           INT         PRIMARY KEY,
                creator_uid   INT         NOT NULL,
                title         VARCHAR(50) NOT NULL,
                type          VARCHAR(50) NOT NULL,
                datetime      DATETIME    NOT NULL,
                FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Venue (
                vid    INT         PRIMARY KEY,
                street VARCHAR(50) NOT NULL,
                city   VARCHAR(50) NOT NULL,
                state  CHAR(2)     NOT NULL,
                zip    CHAR(5)     NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OnCampus (
                vid  INT         PRIMARY KEY,
                code VARCHAR(20) NOT NULL,
                FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OffCampus (
                vid INT PRIMARY KEY,
                distance INT NOT NULL,
                FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Slot (
                snum        INT,
                eid         INT,
                is_reserved BOOLEAN DEFAULT FALSE,
                uid         INT,
                PRIMARY KEY (snum, eid),
                FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
                FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Hosting (
                eid INT,
                vid INT,
                is_primary BOOLEAN NOT NULL,
                PRIMARY KEY(eid, vid),
                FOREIGN KEY(eid) REFERENCES Event(eid) ON DELETE CASCADE,
                FOREIGN KEY(vid) REFERENCES Venue(vid) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Approval (
                uid         INT,
                vid         INT,
                valid_from  DATE NOT NULL,
                valid_until DATE NOT NULL,
                PRIMARY KEY (uid, vid),
                FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
                FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
            )
        """)

        conn.commit()
    
    except Exception as e:
        print(f"create_table failed: {e}")
    finally:
        cursor.close()
        conn.close()

def load_csv(file_path: str, columns: list) -> list[dict]:
    """
    Reads a CSV file and returns a list of row dicts.
    Keys are taken from the header row.
    """
    rows = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=columns)
        for row in reader:
            rows.append(row)
    return rows

def import_data(data_directory: str) -> bool:
    """
    Imports all of the csv files into SQL data tables.
    On fail, it will print the exception and return False.
    On success, it returns True.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS Approval")
        cursor.execute("DROP TABLE IF EXISTS Hosting")
        cursor.execute("DROP TABLE IF EXISTS Slot")
        cursor.execute("DROP TABLE IF EXISTS OffCampus")
        cursor.execute("DROP TABLE IF EXISTS OnCampus")
        cursor.execute("DROP TABLE IF EXISTS Venue")
        cursor.execute("DROP TABLE IF EXISTS Event")
        cursor.execute("DROP TABLE IF EXISTS Administrator")
        cursor.execute("DROP TABLE IF EXISTS Participant")
        cursor.execute("DROP TABLE IF EXISTS Organizer")
        cursor.execute("DROP TABLE IF EXISTS User")

        create_tables()
        
        # User (uid, email, username, joined)
        for row in load_csv(f"{data_directory}/User.csv", ["uid", "email", "username", "joined"]):
            cursor.execute(
                "INSERT INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
                (_clean(row["uid"]), _clean(row["email"]), _clean(row["username"]), _clean(row["joined"]))
            )

        # Organizer (uid, department, experience)
        for row in load_csv(f"{data_directory}/Organizer.csv", ["uid", "department", "experience"]):
            cursor.execute(
                "INSERT INTO Organizer (uid, department, experience) VALUES (%s, %s, %s)",
                (_clean(row["uid"]), _clean(row["department"]), _clean(row["experience"]))
            )

        # Participant (uid, type)
        for row in load_csv(f"{data_directory}/Participant.csv", ["uid", "type"]):
            cursor.execute(
                "INSERT INTO Participant (uid, type) VALUES (%s, %s)",
                (_clean(row["uid"]), _clean(row["type"]))
            )

        # Administrator (uid, firstname, lastname)
        for row in load_csv(f"{data_directory}/Administrator.csv", ["uid", "firstname", "lastname"]):
            cursor.execute(
                "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
                (_clean(row["uid"]), _clean(row["firstname"]), _clean(row["lastname"]))
            )

        # Event (eid, creator_uid, title, type, datetime)
        for row in load_csv(f"{data_directory}/Event.csv", ["eid", "creator_uid", "title", "type", "datetime"]):
            cursor.execute(
                "INSERT INTO Event (eid, creator_uid, title, type, datetime) VALUES (%s, %s, %s, %s, %s)",
                (_clean(row["eid"]), _clean(row["creator_uid"]), _clean(row["title"]), _clean(row["type"]), _clean(row["datetime"]))
            )

        # Venue (vid, street, city, state, zip)
        for row in load_csv(f"{data_directory}/Venue.csv", ["vid", "street", "city", "state", "zip"]):
            cursor.execute(
                "INSERT INTO Venue (vid, street, city, state, zip) VALUES (%s, %s, %s, %s, %s)",
                (_clean(row["vid"]), _clean(row["street"]), _clean(row["city"]), _clean(row["state"]), _clean(row["zip"]))
            )

        # OnCampus (vid, code)
        for row in load_csv(f"{data_directory}/OnCampus.csv", ["vid", "code"]):
            cursor.execute(
                "INSERT INTO OnCampus (vid, code) VALUES (%s, %s)",
                (_clean(row["vid"]), _clean(row["code"]))
            )

        # OffCampus (vid, distance)
        for row in load_csv(f"{data_directory}/OffCampus.csv", ["vid", "distance"]):
            cursor.execute(
                "INSERT INTO OffCampus (vid, distance) VALUES (%s, %s)",
                (_clean(row["vid"]), _clean(row["distance"]))
            )

        # Slot (eid, snum, is_reserved)
        for row in load_csv(f"{data_directory}/Slot.csv", ["eid", "snum", "is_reserved", "uid"]):
            cursor.execute(
                "INSERT INTO Slot (eid, snum, is_reserved, uid) VALUES (%s, %s, %s, %s)",
                (_clean(row["eid"]), _clean(row["snum"]), _clean(row["is_reserved"]), _clean(row["uid"]))
            )

        # Hosting (eid, vid, is_primary)
        for row in load_csv(f"{data_directory}/Hosting.csv", ["eid", "vid", "is_primary"]):
            cursor.execute(
                "INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
                (_clean(row["eid"]), _clean(row["vid"]), _clean(row["is_primary"]))
            )

        # Approval (vid, uid, valid_from, valid_until)
        for row in load_csv(f"{data_directory}/Approval.csv", ["uid", "vid", "valid_from", "valid_until"]):
            cursor.execute(
                "INSERT INTO Approval (uid, vid, valid_from, valid_until) VALUES (%s, %s, %s, %s)",
                (_clean(row["uid"]), _clean(row["vid"]), _clean(row["valid_from"]), _clean(row["valid_until"]))
            )

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Import failed: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
