# Configuraciones principales

import secrets
from mysql.connector import Error
import mysql.connector

# Generar clave secreta
class Config:
    SECRET_KEY = secrets.token_hex(50)

# Crear la conexion
def create_connection():
    """ Craer la conexion con la base de datos MySQL """

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='elmer',
            password='11119gM9*g2516v0512>>o37Ri27',
            database='VerdeNica'
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection