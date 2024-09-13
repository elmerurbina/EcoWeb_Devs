from settings import create_connection
from mysql.connector import Error


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
