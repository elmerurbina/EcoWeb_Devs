from settings import create_connection
from mysql.connector import Error
import bcrypt
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, nombre, correo, contrasenia, profile_photo):
        self.id = user_id
        self.nombre = nombre
        self.correo = correo
        self.contrasenia = contrasenia
        self.profile_photo = profile_photo or 'profile-placeholder.jpeg'

    @staticmethod
    def get(user_id):
        """Fetch user by ID from the database."""
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT id, nombre, correo, contrasenia, profile_photo FROM sistemaautenticacion WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                return User(result[0], result[1], result[2], result[3], result[4])  # Return a User instance
            return None
        except Error as e:
            print(f"The error '{e}' occurred")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# Function to register a new user
def register_user(nombre, correo, contrasenia):
    """registrar un nuevo usuario utilizando un procedure almacenado."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(contrasenia.encode(), bcrypt.gensalt())

        # Call the stored procedure
        cursor.callproc('RegisterUser', (nombre, correo, hashed_password.decode()))
        connection.commit()
        print("User registered successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to validate login credentials
def check_login(correo, contrasenia):
    """Validate login credentials using a stored procedure."""
    connection = create_connection()
    cursor = connection.cursor()
    user = None
    try:
        # Call the stored procedure
        cursor.callproc('CheckLogin', (correo,))

        # Retrieve the result from the stored procedure
        for result in cursor.stored_results():
            row = result.fetchone()  # Fetch the first row from the result
            if row:
                stored_password = row[3]  # Assuming contrasenia is at index 3
                if bcrypt.checkpw(contrasenia.encode(), stored_password.encode()):
                    user = row
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
