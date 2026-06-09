from db import get_connection

def insertAdmin(uid, email, username, joined, firstname, lastname):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
            (uid, email, username, joined)
        )
        cursor.execute(
            "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
            (uid, firstname, lastname)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"insertAdmin failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def updateEvent(eid, title=None, type=None, datetime=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Event WHERE eid = %s", (eid,))
        if cursor.fetchone() is None:
            return False
        cursor.execute(
            "UPDATE Event SET title=%s, type=%s, datetime=%s WHERE eid=%s",
            (title, type, datetime, eid)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"updateEvent failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def deleteOrganizer(uid):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Organizer WHERE uid = %s", (uid,))
        if cursor.fetchone() is None:
            return False
        cursor.execute("DELETE FROM Organizer WHERE uid = %s", (uid,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()