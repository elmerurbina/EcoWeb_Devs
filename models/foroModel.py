from settings import create_connection
from mysql.connector import Error

# Funciones para debates
def get_debate_by_id(debate_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    debate = None
    try:
        query = "SELECT * FROM foro_debates WHERE id = %s"
        cursor.execute(query, (debate_id,))
        debate = cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return debate


def update_debate(debate_id, titulo, descripcion, punto_de_vista, otras_observaciones, autor_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE foro_debates
            SET titulo = %s, descripcion = %s, punto_de_vista = %s, otras_observaciones = %s, autor_id = %s
            WHERE id = %s
        """
        cursor.execute(query, (titulo, descripcion, punto_de_vista, otras_observaciones, autor_id, debate_id))
        connection.commit()
        print("Debate updated successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_debate(debate_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM foro_debates WHERE id = %s"
        cursor.execute(query, (debate_id,))
        connection.commit()
        print("Debate deleted successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Funciones similares para preguntas
def get_question_by_id(question_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    question = None
    try:
        query = "SELECT * FROM foro_preguntas WHERE id = %s"
        cursor.execute(query, (question_id,))
        question = cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return question

def update_question(question_id, titulo, pregunta, autor_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE foro_preguntas
            SET titulo = %s, pregunta = %s, autor_id = %s
            WHERE id = %s
        """
        cursor.execute(query, (titulo, pregunta, autor_id, question_id))
        connection.commit()
        print("Question updated successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_question(question_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM foro_preguntas WHERE id = %s"
        cursor.execute(query, (question_id,))
        connection.commit()
        print("Question deleted successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Funciones similares para hilos de conversación
def get_thread_by_id(thread_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    thread = None
    try:
        query = "SELECT * FROM foro_hilos WHERE id = %s"
        cursor.execute(query, (thread_id,))
        thread = cursor.fetchone()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return thread

def get_all_questions():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    questions = []
    try:
        query = """
            SELECT q.*, u.nombre as autor
            FROM foro_preguntas q
            JOIN sistemaautenticacion u ON q.autor_id = u.id
            ORDER BY q.fecha_creacion DESC
        """
        cursor.execute(query)
        questions = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return questions

def get_all_threads():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    threads = []
    try:
        query = """
            SELECT t.*, u.nombre as autor
            FROM foro_hilos t
            JOIN sistemaautenticacion u ON t.autor_id = u.id
            ORDER BY t.fecha_creacion DESC
        """
        cursor.execute(query)
        threads = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return threads

def update_thread(thread_id, titulo, tema, autor_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = """
            UPDATE foro_hilos
            SET titulo = %s, tema = %s, autor_id = %s
            WHERE id = %s
        """
        cursor.execute(query, (titulo, tema, autor_id, thread_id))
        connection.commit()
        print("Thread updated successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_thread(thread_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM foro_hilos WHERE id = %s"
        cursor.execute(query, (thread_id,))
        connection.commit()
        print("Thread deleted successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Actualizar las clases para incluir autor_id
class ForoDebate:
    def __init__(self, titulo, descripcion, punto_de_vista, otras_observaciones='', autor_id=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.punto_de_vista = punto_de_vista
        self.otras_observaciones = otras_observaciones
        self.autor_id = autor_id

    @staticmethod
    def save(titulo, descripcion, punto_de_vista, otras_observaciones='', autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO foro_debates (titulo, descripcion, punto_de_vista, otras_observaciones, autor_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (titulo, descripcion, punto_de_vista, otras_observaciones, autor_id))
            connection.commit()
            print("Debate saved successfully")
        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class ForoPregunta:
    def __init__(self, titulo, pregunta, autor_id=None):
        self.titulo = titulo
        self.pregunta = pregunta
        self.autor_id = autor_id

    @staticmethod
    def save(titulo, pregunta, autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO foro_preguntas (titulo, pregunta, autor_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (titulo, pregunta, autor_id))
            connection.commit()
            print("Question saved successfully")
        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class ForoHilo:
    def __init__(self, titulo, tema, autor_id=None):
        self.titulo = titulo
        self.tema = tema
        self.autor_id = autor_id

    @staticmethod
    def save(titulo, tema, autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO foro_hilos (titulo, tema, autor_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (titulo, tema, autor_id))
            connection.commit()
            print("Thread saved successfully")
        except Error as e:
            print(f"Error: {e}")
            raise e
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Actualizar las funciones para obtener todos los debates, preguntas y hilos
def get_all_debates():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    debates = []
    try:
        query = """
            SELECT d.*, u.nombre as autor
            FROM foro_debates d
            JOIN sistemaautenticacion u ON d.autor_id = u.id
            ORDER BY d.fecha_creacion DESC
        """
        cursor.execute(query)
        debates = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return debates

# Actualizar la función para guardar respuestas
def save_response(respuesta, item_id, item_type, autor_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        if item_type == 'debate':
            query = "INSERT INTO foro_respuestas_debate (respuesta, debate_id, autor_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (respuesta, item_id, autor_id))
        elif item_type == 'pregunta':
            query = "INSERT INTO foro_respuestas_pregunta (respuesta, pregunta_id, autor_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (respuesta, item_id, autor_id))
        connection.commit()
        print("Response saved successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_respuestas(item_id, item_type):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    respuestas = []
    try:
        if item_type == 'debate':
            query = """
                SELECT r.*, u.nombre as autor
                FROM foro_respuestas_debate r
                JOIN sistemaautenticacion u ON r.autor_id = u.id
                WHERE r.debate_id = %s
                ORDER BY r.fecha_creacion DESC
            """
            cursor.execute(query, (item_id,))
        elif item_type == 'pregunta':
            query = """
                SELECT r.*, u.nombre as autor
                FROM foro_respuestas_pregunta r
                JOIN sistemaautenticacion u ON r.autor_id = u.id
                WHERE r.pregunta_id = %s
                ORDER BY r.fecha_creacion DESC
            """
            cursor.execute(query, (item_id,))

        respuestas = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return respuestas
