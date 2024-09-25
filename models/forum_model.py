from settings import create_connection
from mysql.connector import Error

# Funciones para debates
def get_debate_by_id(debate_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    debate = None
    try:
        query = "CALL GetDebateByID(%s)"
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
        query = "CALL UpdateDebate(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (debate_id, titulo, descripcion, punto_de_vista, otras_observaciones, autor_id))
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
        query = "CALL DeleteDebate(%s)"
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
def get_question_by_id(pregunta_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.callproc('GetQuestionByID', [pregunta_id])
    for result in cursor.stored_results():
        question = result.fetchall()
    connection.close()
    return question


def update_question(pregunta_id, titulo, cuerpo):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.callproc('UpdateQuestion', [pregunta_id, titulo, cuerpo])
    connection.commit()
    connection.close()

def delete_question(question_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "CALL DeleteQuestion(%s)"
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
def get_thread_by_id(hilo_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.callproc('GetThreadByID', [hilo_id])
    for result in cursor.stored_results():
        thread = result.fetchall()
    connection.close()
    return thread

def get_all_debates():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    debates = []
    try:
        query = "CALL GetAllDebates()"
        cursor.execute(query)
        debates = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return debates

def get_all_questions():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    questions = []
    try:
        query = "CALL GetAllQuestions()"
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
        query = "CALL GetAllThreads()"
        cursor.execute(query)
        threads = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return threads

def update_thread(hilo_id, titulo, contenido):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.callproc('UpdateThread', [hilo_id, titulo, contenido])
    connection.commit()
    connection.close()

def delete_thread(thread_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "CALL DeleteThread(%s)"
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
    @staticmethod
    def save(titulo, descripcion, punto_de_vista, otras_observaciones='', autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "CALL SaveDebate(%s, %s, %s, %s, %s)"
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
    @staticmethod
    def save(titulo, pregunta, autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "CALL SaveQuestion(%s, %s, %s)"
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
    @staticmethod
    def save(titulo, tema, autor_id=None):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            query = "CALL SaveThread(%s, %s, %s)"
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

def save_response(respuesta, item_id, item_type, autor_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "CALL SaveResponse(%s, %s, %s, %s)"
        cursor.execute(query, (respuesta, item_id, item_type, autor_id))
        connection.commit()
        print("Response saved successfully")
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_respuestas(item_id, item_type):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    respuestas = []
    try:
        query = "CALL GetRespuestas(%s, %s)"
        cursor.execute(query, (item_id, item_type))
        respuestas = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return respuestas
