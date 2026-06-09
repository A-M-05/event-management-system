from db import get_connection

def insert_admin(args):
    # args: uid, email, username, joined, firstname, lastname
    conn = get_connection()
    cursor = conn.cursor()
    try:
        uid = int(args[0])
        email = args[1]
        username = args[2]
        joined = args[3]
        firstname = args[4]
        lastname = args[5]

        # User may already exist (covering + overlapping ISA), so use INSERT IGNORE.
        # This skips the User insert if the uid already exists.
        cursor.execute(
            "INSERT IGNORE INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
            (uid, email, username, joined)
        )
        cursor.execute(
            "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
            (uid, firstname, lastname)
        )
        conn.commit()
        print("Success")
    except Exception as e:
        conn.rollback()
        print("Fail")
    finally:
        cursor.close()
        conn.close()

def update_event(args):
    # args: eid, title, datetime
    conn = get_connection()
    cursor = conn.cursor()
    try:
        eid = int(args[0])
        title = args[1]
        datetime = args[2]

        cursor.execute("SELECT * FROM Event WHERE eid = %s", (eid,))
        if cursor.fetchone() is None:
            print("Fail")
            return
        cursor.execute(
            "UPDATE Event SET title=%s, datetime=%s WHERE eid=%s",
            (title, datetime, eid)
        )
        conn.commit()
        print("Success")
    except Exception as e:
        conn.rollback()
        print("Fail")
    finally:
        cursor.close()
        conn.close()

def delete_organizer(args):
    # args: uid
    conn = get_connection()
    cursor = conn.cursor()
    try:
        uid = int(args[0])

        cursor.execute("SELECT * FROM Organizer WHERE uid = %s", (uid,))
        if cursor.fetchone() is None:
            print("Fail")
            return
        # ON DELETE CASCADE handles Events, Slots, and Hosting automatically
        cursor.execute("DELETE FROM Organizer WHERE uid = %s", (uid,))
        conn.commit()
        print("Success")
    except Exception:
        conn.rollback()
        print("Fail")
    finally:
        cursor.close()
        conn.close()