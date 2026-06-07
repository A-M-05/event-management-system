import csv
from db import get_connection

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
        # User (uid, email, username, joined)
        for row in load_csv(f"{data_directory}/User.csv", ["uid", "email", "username", "joined"]):
            cursor.execute(
                "INSERT IGNORE INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
                (row["uid"], row["email"], row["username"], row["joined"])
            )

        # Organizer (uid, department, experience)
        for row in load_csv(f"{data_directory}/Organizer.csv", ["uid", "department", "experience"]):
            cursor.execute(
                "INSERT IGNORE INTO Organizer (uid, department, experience) VALUES (%s, %s, %s)",
                (row["uid"], row["department"], row["experience"])
            )

        # Participant (uid, type)
        for row in load_csv(f"{data_directory}/Participant.csv", ["uid", "type"]):
            cursor.execute(
                "INSERT IGNORE INTO Participant (uid, type) VALUES (%s, %s)",
                (row["uid"], row["type"])
            )

        # Administrator (uid, firstname, lastname)
        for row in load_csv(f"{data_directory}/Administrator.csv", ["uid", "firstname", "lastname"]):
            cursor.execute(
                "INSERT IGNORE INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
                (row["uid"], row["firstname"], row["lastname"])
            )

        # Event (eid, creator_uid, title, type, datetime)
        for row in load_csv(f"{data_directory}/Event.csv", ["eid", "creator_uid", "title", "type", "datetime"]):
            cursor.execute(
                "INSERT IGNORE INTO Event (eid, creator_uid, title, type, datetime) VALUES (%s, %s, %s, %s, %s)",
                (row["eid"], row["creator_uid"], row["title"], row["type"], row["datetime"])
            )

        # Venue (vid, street, city, state, zip)
        for row in load_csv(f"{data_directory}/Venue.csv", ["vid", "street", "city", "state", "zip"]):
            cursor.execute(
                "INSERT IGNORE INTO Venue (vid, street, city, state, zip) VALUES (%s, %s, %s, %s, %s)",
                (row["vid"], row["street"], row["city"], row["state"], row["zip"])
            )

        # OnCampus (vid, code)
        for row in load_csv(f"{data_directory}/OnCampus.csv", ["vid", "code"]):
            cursor.execute(
                "INSERT IGNORE INTO OnCampus (vid, code) VALUES (%s, %s)",
                (row["vid"], row["code"])
            )

        # OffCampus (vid, distance)
        for row in load_csv(f"{data_directory}/OffCampus.csv", ["vid", "distance"]):
            cursor.execute(
                "INSERT IGNORE INTO OffCampus (vid, distance) VALUES (%s, %s)",
                (row["vid"], row["distance"])
            )

        # Slot (eid, snum, is_reserved)
        for row in load_csv(f"{data_directory}/Slot.csv", ["eid", "snum", "is_reserved", "uid"]):
            cursor.execute(
                "INSERT IGNORE INTO Slot (eid, snum, is_reserved, uid) VALUES (%s, %s, %s, %s)",
                (row["eid"], row["snum"], row["is_reserved"], row.get("uid") or None)
            )

        # Hosting (eid, vid, is_primary)
        for row in load_csv(f"{data_directory}/Hosting.csv", ["eid", "vid", "is_primary"]):
            cursor.execute(
                "INSERT IGNORE INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
                (row["eid"], row["vid"], row["is_primary"])
            )

        # Approval (vid, uid, valid_from, valid_until)
        for row in load_csv(f"{data_directory}/Approval.csv", ["uid", "vid", "valid_from", "valid_until"]):
            cursor.execute(
                "INSERT IGNORE INTO Approval (uid, vid, valid_from, valid_until) VALUES (%s, %s, %s, %s)",
                (row["uid"], row["vid"], row["valid_from"], row["valid_until"])
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