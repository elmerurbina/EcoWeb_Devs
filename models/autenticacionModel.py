from config import create_connection
from mysql.connector import Error
import bcrypt


# Funcion para registrar a un nuevo usuario
def register_user(nombre, correo, contrasenia):
    """Register a new user in the database."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(contrasenia.encode(), bcrypt.gensalt())

        query = "INSERT INTO sistemaautenticacion (nombre, correo, contrasenia) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, correo, hashed_password))
        connection.commit()
        print("User registered successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Funcion para validar las credenciales de inicio de sesion
def check_login(correo, contrasenia):
    """Verify user credentials."""
    connection = create_connection()
    cursor = connection.cursor()
    user = None
    try:
        query = "SELECT correo, contrasenia FROM sistemaautenticacion WHERE correo = %s"
        cursor.execute(query, (correo,))
        result = cursor.fetchone()

        if result:
            stored_password = result[1]
            print(f"Stored password hash: {stored_password}")
            print(f"Password to check: {contrasenia}")

            # Check if the password matches
            if bcrypt.checkpw(contrasenia.encode(), stored_password.encode()):
                print(f"User found: {result}")
                user = result
            else:
                print("Invalid credentials")
        else:
            print("User not found")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return user
