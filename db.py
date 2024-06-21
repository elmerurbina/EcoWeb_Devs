import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to the MySQL database """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='7>>HhNN6/fZ',
            database='clima_sostenible'
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def register_user(nombre, correo, contrasenia):
    """ Register a new user in the database """
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO sistemaAutenticacion (nombre, correo, contrasenia) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, correo, contrasenia))
        connection.commit()
        print("User registered successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def check_login(correo, contrasenia):
    """ Check user login credentials """
    connection = create_connection()
    cursor = connection.cursor()
    user = None
    try:
        query = "SELECT * FROM sistemaAutenticacion WHERE correo = %s AND contrasenia = %s"
        cursor.execute(query, (correo, contrasenia))
        user = cursor.fetchone()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return user
