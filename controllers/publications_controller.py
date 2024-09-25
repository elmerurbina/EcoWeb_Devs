# Archivo para manejar la logica de las publicaciones

# Importacion de librerias y modulos
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
import uuid
from settings import Config, create_connection
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Directorio para guardar las images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ruta para manejar una nueva publicacion creada por el usuario
@app.route('/submit_publication', methods=['GET', 'POST'])
def submit_publication():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        image_file = request.files['image']

        # Manejar el archivo de la imagen si se proporciono
        if image_file and image_file.filename != '':
            # Asegurarse que el archivo sea seguro y que no exista en el directorio de uploads
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(image_path)


            image_path = os.path.join('../uploads', unique_filename)
        else:
            image_path = None  # En caso de que no se suba una imagen

        # Guardar la publicacion en la base de datos
        cursor = create_connection().cursor()
        sql = """
            INSERT INTO publicaciones (title, category, content, image, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        cursor.execute(sql, (title, category, content, image_path, created_at))
        create_connection().commit()

        flash('Publicación creada con éxito', 'success')
        return redirect(url_for('publicaciones'))

    return render_template('new_publication.html')

# Ruta para la interfaz principal
@app.route('/publications')
def publications():
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM publicaciones ORDER BY created_at DESC")
        publications = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return jsonify({'error': 'Failed to execute query'}), 500
    finally:
        cursor.close()
        conn.close()

    return render_template('publications.html', publications=publications)

if __name__ == '__main__':
    app.run(debug=True)
