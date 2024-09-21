from settings import create_connection
from mysql.connector import Error

# Function to update a user's profile
from settings import create_connection
from mysql.connector import Error

# Function to update a user's profile
def update_profile(user_id, nombre, correo, contrasenia=None, profile_photo=None):
    """Actualizar perfil utilizando un procedure almacenado."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Call the stored procedure
        if contrasenia:
            cursor.callproc('UpdateUserProfile', (user_id, nombre, correo, contrasenia, profile_photo))
        else:
            cursor.callproc('UpdateUserProfile', (user_id, nombre, correo, None, profile_photo))

        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to delete a user profile

def delete_user(user_id):

    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Call the stored procedure
        cursor.callproc('DeleteUserProfile', (user_id,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

