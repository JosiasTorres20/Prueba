import mysql.connector

def get_db():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = "",
        database="empresa"
    )
    return connection