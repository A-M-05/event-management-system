"""Read-only query operations for the ZotEvent platform.

Each function executes a SELECT query and prints results in CSV format
(one record per line, comma-separated columns).
"""
from db import get_connection
import datetime


def _format(value):
    """Format a single value for CSV-style output.
    
    Converts None to empty string, everything else to its str() form.
    """
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    
    return str(value)


def _print_rows(cursor):
    """Print each row from the cursor as a comma-separated line."""
    for row in cursor.fetchall():
        print(",".join(_format(v) for v in row))


def available_events(date):
    """List future events with at least one unreserved slot."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                    """
                    SELECT E.eid, E.title, E.type, E.datetime, COUNT(S.snum) AS availableSlots
                    FROM Event E
                    INNER JOIN Slot S ON S.eid = E.eid
                    WHERE E.datetime > %s AND S.is_reserved = FALSE
                    GROUP BY E.eid, E.title, E.type, E.datetime
                    ORDER BY E.datetime ASC, E.eid ASC
                    """, (date, ))
        _print_rows(cursor)
    finally:
        cursor.close()
        conn.close()


def popular_event_types(n):
    """For each event type, count reserved slots; filter by >= N."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                    """
                    SELECT E.type, COUNT(S.snum) AS reservedCount
                    FROM Event E
                    INNER JOIN Slot S ON S.eid = E.eid
                    WHERE S.is_reserved = TRUE
                    GROUP BY E.type
                    HAVING COUNT(S.snum) >= %s
                    ORDER BY reservedCount DESC, E.type ASC
                    """, (n, ))
        _print_rows(cursor)
    finally:
        cursor.close()
        conn.close()


def participant_schedule(uid):
    """List events a participant has reserved, with primary venue info."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                    """
                    SELECT DISTINCT E.eid, E.title, E.type, E.datetime, S.snum, V.vid, V.street, V.city, V.state, V.zip
                    FROM Event E
                    INNER JOIN Slot S ON S.eid = E.eid AND S.uid = %s
                    LEFT JOIN Hosting H ON E.eid = H.eid AND H.is_primary = TRUE
                    LEFT JOIN Venue V on H.vid = V.vid
                    ORDER BY E.datetime ASC, E.eid ASC
                    """, (uid, ))
        _print_rows(cursor)
    finally:
        cursor.close()
        conn.close()


def organizer_stats(n):
    """List organizers with at least N events."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                    """
                    SELECT O.uid, U.username, O.department, COUNT(E.eid) AS eventCount
                    FROM Organizer O
                    INNER JOIN User U ON U.uid = O.uid
                    INNER JOIN Event E ON E.creator_uid = O.uid
                    GROUP BY O.uid, U.username, O.department
                    HAVING COUNT(E.eid) >= %s
                    ORDER BY eventCount DESC, O.uid ASC
                    """, (n, ))
        _print_rows(cursor)
    finally:
        cursor.close()
        conn.close()


def venue_events(vid):
    """List events at a venue with is_primary flag."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
                    """
                    SELECT E.eid, E.title, E.type, E.datetime, H.is_primary
                    FROM Event E
                    INNER JOIN Hosting H ON E.eid = H.eid
                    WHERE H.vid = %s
                    ORDER BY E.datetime ASC, E.eid ASC
                    """, (vid, ))
        _print_rows(cursor)
    finally:
        cursor.close()
        conn.close()
