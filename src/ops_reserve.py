from db import get_connection


def str_to_bool(s):
    return str(s).lower() == "true"


def add_venue(args):
    # args: eid, vid, is_primary
    conn = None

    try:
        eid = int(args[0])
        vid = int(args[1])
        is_primary = str_to_bool(args[2])

        conn = get_connection()
        cursor = conn.cursor()

        # if this is a primary venue, check if the event already has one
        if is_primary:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM Hosting
                WHERE eid = %s AND is_primary = TRUE
                """,
                (eid,)
            )

            count = cursor.fetchone()[0]

            if count > 0:
                print("Fail")
                return

        cursor.execute(
            """
            INSERT INTO Hosting (eid, vid, is_primary)
            VALUES (%s, %s, %s)
            """,
            (eid, vid, is_primary)
        )

        conn.commit()
        print("Success")

    except:
        if conn:
            conn.rollback()
        print("Fail")

    finally:
        if conn:
            conn.close()


def reserve_slot(args):
    # args: eid, snum, uid
    conn = None

    try:
        eid = int(args[0])
        snum = int(args[1])
        uid = int(args[2])

        conn = get_connection()
        cursor = conn.cursor()

        # only reserve the slot if it is not already reserved
        cursor.execute(
            """
            UPDATE Slot
            SET is_reserved = TRUE, uid = %s
            WHERE eid = %s
              AND snum = %s
              AND is_reserved = FALSE
            """,
            (uid, eid, snum)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            print("Fail")
            return

        conn.commit()
        print("Success")

    except:
        if conn:
            conn.rollback()
        print("Fail")

    finally:
        if conn:
            conn.close()


def cancel_reservation(args):
    # args: eid, snum, uid
    conn = None

    try:
        eid = int(args[0])
        snum = int(args[1])
        uid = int(args[2])

        conn = get_connection()
        cursor = conn.cursor()

        # only cancel if this user is the one who reserved the slot
        cursor.execute(
            """
            UPDATE Slot
            SET is_reserved = FALSE, uid = NULL
            WHERE eid = %s
              AND snum = %s
              AND uid = %s
              AND is_reserved = TRUE
            """,
            (eid, snum, uid)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            print("Fail")
            return

        conn.commit()
        print("Success")

    except:
        if conn:
            conn.rollback()
        print("Fail")

    finally:
        if conn:
            conn.close()