from settings import create_connection
from mysql.connector import Error

# Function to update a user's profile
def update_profile(user_id, nombre, correo, contrasenia=None, profile_photo=None):
    """Update user profile in the database."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if contrasenia:
            # If password is provided, update name, email, and password
            query = "UPDATE sistemaautenticacion SET nombre = %s, correo = %s, contrasenia = %s, profile_photo = %s WHERE id = %s"
            cursor.execute(query, (nombre, correo, contrasenia, profile_photo, user_id))
        else:
            # If password is not provided, update only name, email, and profile photo
            query = "UPDATE sistemaautenticacion SET nombre = %s, correo = %s, profile_photo = %s WHERE id = %s"
            cursor.execute(query, (nombre, correo, profile_photo, user_id))

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
    """Delete user profile from the database."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM sistemaautenticacion WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
