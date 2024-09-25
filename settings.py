# Configuraciones principales

import secrets
from flask import Flask
from mysql.connector import Error
import mysql.connector

app = Flask(__name__)

# Generar clave secreta
class Config:
    SECRET_KEY = secrets.token_hex(50)



# Crear conexion con la base de datos
def create_connection():
    """Create a connection with the MySQL database."""
    connection = None
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