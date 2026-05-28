import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="password",
        database="zotevent"
    )

    return conn