from settings import create_connection
from mysql.connector import Error

# Funcion para guardar las campanias en la base de datos
def save_campaign(nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto=None):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        if presupuesto == '':  # Si el campo de presupuesto esta vacio
            presupuesto = None  # Se convierte a None

        # Llamar el procedure almacenado con o sin el presupuesto
        if presupuesto is not None:
            cursor.callproc('SaveCampaign', (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, presupuesto))
        else:
            cursor.callproc('SaveCampaign', (nombre_campania, descripcion_campania, fecha_inicio, fecha_fin, None))

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
        # Call the stored procedure to get all campaigns
        cursor.callproc('GetAllCampaigns')
        for result in cursor.stored_results():
            campaigns = result.fetchall()

        # Get comments for each campaign
        for campaign in campaigns:
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
        # Call the stored procedure to get comments for the given campaign
        cursor.callproc('GetCommentsForCampaign', (campaign_id,))
        for result in cursor.stored_results():
            comments = result.fetchall()

        return comments
    except Error as e:
        print(f"The error '{e}' occurred")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



# Function to save the comment on the database
def save_comment(campaign_id, comment_text):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Call the stored procedure to save a comment
        cursor.callproc('SaveComment', (campaign_id, comment_text))
        connection.commit()
        print("Comment saved successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
