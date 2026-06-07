import mysql.connector


def get_connection():
    return mysql.connector.connect(
        user="test",
        password="password",
        database="cs122a"
    )
