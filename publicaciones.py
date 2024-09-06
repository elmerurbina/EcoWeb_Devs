# Archivo para manejar la logica de las publicaciones

# Importacion de librerias y modulos
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Directorio para guardar las imagenes
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Generar la conexion con la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7>>HhNN6/fZ",
    database="VerdeNica"
)

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


            image_path = os.path.join('uploads', unique_filename)
        else:
            image_path = None  # En caso de que no se suba una imagen

        # Guardar la publicacion en la base de datos
        cursor = db.cursor()
        sql = """
            INSERT INTO publicaciones (title, category, content, image, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        cursor.execute(sql, (title, category, content, image_path, created_at))
        db.commit()

        flash('Publicación creada con éxito', 'success')
        return redirect(url_for('publicaciones'))

    return render_template('new_publication.html')

# Ruta para la interfaz principal
@app.route('/publicaciones')
def publicaciones():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM publicaciones ORDER BY created_at DESC") # Las publicaciones de ordenan en orden de mas reciente
    publications = cursor.fetchall()
    return render_template('publicaciones.html', publications=publications)

if __name__ == '__main__':
    app.run(debug=True)
