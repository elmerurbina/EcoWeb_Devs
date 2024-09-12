# Archivo para manejar la conexion con la base de datos y los metodos

# Librerias
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime

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

# Funcion para guardar las respuestas del Foro
def save_response(respuesta):
    try:
        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        query = '''
            INSERT INTO respuestas (respuesta) 
            VALUES (%s)
        '''


        cursor.execute(query, (respuesta,))

        connection.commit()
        print("Response saved successfully")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Funcion para acceder a las respuestas del Foro guardadas en la base de datos
def get_respuestas():
    conn = create_connection()
    respuestas = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM respuestas ORDER BY fecha DESC') # Ordenar las respuestas en orden de mas reciente
        respuestas = cursor.fetchall()
        cursor.close()
        conn.close()
    return respuestas


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


# Clase para manejar la insercion de datos de los debates del foro
class ForoDebate:
    def __init__(self, titulo, descripcion, punto_de_vista, otras_observaciones=''):
        self.titulo = titulo
        self.descripcion = descripcion
        self.punto_de_vista = punto_de_vista
        self.otras_observaciones = otras_observaciones

    @staticmethod
    def save(titulo, descripcion, punto_de_vista, otras_observaciones=''):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO foro_debates (titulo, descripcion, punto_de_vista, otras_observaciones) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (titulo, descripcion, punto_de_vista, otras_observaciones))
            connection.commit()
            print("Debate saved successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Clase para la insercion de datos de las preguntas del foro
class ForoPregunta:
    def __init__(self, titulo, pregunta):
        self.titulo = titulo
        self.pregunta = pregunta

    @staticmethod
    def save(titulo, pregunta):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO foro_preguntas (titulo, pregunta) VALUES (%s, %s)"
            cursor.execute(query, (titulo, pregunta))
            connection.commit()
            print("Question saved successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Clase para la insercion de datos de los hilos de conversacion
class ForoHilo:
    def __init__(self, titulo, tema):
        self.titulo = titulo
        self.tema = tema

    @staticmethod
    def save(titulo, tema):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO foro_hilos (titulo, tema) VALUES (%s, %s)"
            cursor.execute(query, (titulo, tema))
            connection.commit()
            print("Thread saved successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


# Funcion para guardar las campanias en la base de datos
def save_campaign(nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto=None):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        if presupuesto == '': # Si el campo presupuesto esta vacio
            presupuesto = None  # Convertir la variable vacia a None

        # Si el presupuesto no esta vacio
        if presupuesto is not None:
            query = "INSERT INTO campaign (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto))
        else:
            # Si el campo del presupuesto esta vacio
            query = "INSERT INTO campaign (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin))

        connection.commit()
        print("Campaign saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


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

# Funcion para obtener los debates guardados en la base de datos
def get_all_debates():

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    debates = []
    try:
        query = "SELECT * FROM foro_debates ORDER BY fecha_creacion DESC"
        cursor.execute(query)
        debates = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return debates


# Funcion para obtener las preguntas guardadas en la base de datos
def get_all_questions():

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    questions = []
    try:
        query = "SELECT * FROM foro_preguntas ORDER BY fecha_creacion DESC"
        cursor.execute(query)
        questions = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return questions


# Funcion para obtener los hilos de conversacion guardados en la base de datos
def get_all_threads():

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    threads = []
    try:
        query = "SELECT * FROM foro_hilos ORDER BY fecha_creacion DESC"
        cursor.execute(query)
        threads = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return threads

# Funcion para obtener las campanias guardadas en la base de datos
def get_all_campaigns():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM campaign")
        campaigns = cursor.fetchall()

        for campaign in campaigns:
            # Obtener los comentarios por el ID de la campania
            campaign['comments'] = get_comments_for_campaign(campaign['id'])

        return campaigns
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Funcion para obtener los comentarios guardados en la  base de datos
def get_comments_for_campaign(campaign_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM comments WHERE campaign_id = %s", (campaign_id,))
        comments = cursor.fetchall()
        return comments
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Funcion para guardar los comentarios en la base de datos
def save_comment(campaign_id, comment_text):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO comments (campaign_id, comment_text) VALUES (%s, %s)"
        cursor.execute(query, (campaign_id, comment_text))
        connection.commit()
        print("Comment saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        raise
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



