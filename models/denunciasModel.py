from settings import create_connection
from mysql.connector import Error

# Funcion para guardar las denuncias en la base dedatos
def save_denuncia(titulo, descripcion, evidencia_filename, ubicacion, denunciados, otros_detalles=None):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO denuncias (titulo, descripcion, evidencia_filename, ubicacion, denunciados, otros_detalles) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (titulo, descripcion, evidencia_filename, ubicacion, denunciados, otros_detalles))
        connection.commit()
        print("Denuncia saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



# Funcion para obtener las denuncias guardadas en la base de datos
def get_all_denuncias():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Updated SQL query to order by fecha_creacion in descending order
        cursor.execute("SELECT * FROM denuncias ORDER BY fecha_creacion DESC")
        denuncias = cursor.fetchall()
        return denuncias
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
