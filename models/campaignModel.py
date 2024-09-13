from config import create_connection
from mysql.connector import Error

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
