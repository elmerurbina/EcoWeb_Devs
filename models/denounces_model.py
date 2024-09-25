from settings import create_connection
from mysql.connector import Error

# Function to save a "denuncia" using a stored procedure
def save_denuncia(titulo, descripcion, evidencia_filename, ubicacion, denunciados, otros_detalles=None):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Call the stored procedure to save a "denuncia"
        cursor.callproc('SaveDenuncia', (titulo, descripcion, evidencia_filename, ubicacion, denunciados, otros_detalles))
        connection.commit()
        print("Denuncia saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



# Obtain all the existing denounces on the database
def get_all_denuncias():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Call the stored procedure to retrieve all "denuncias"
        cursor.callproc('GetAllDenuncias')
        for result in cursor.stored_results():
            denuncias = result.fetchall()
        return denuncias
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
