from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL database connection setup
db = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="root",  # Replace with your MySQL user
    password="7>>HhNN6/fZ",  # Replace with your MySQL password
    database="VerdeNica"  # Name of your database
)

@app.route('/submit_publication', methods=['GET', 'POST'])
def submit_publication():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        image_file = request.files['image']

        # Handle image upload if provided
        if image_file and image_file.filename != '':
            # Ensure filename is secure and unique by appending a UUID
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(image_path)

            # Store relative image path (used for HTML rendering)
            image_path = os.path.join('uploads', unique_filename)
        else:
            image_path = None  # No image uploaded

        # Insert the publication into the MySQL database with created_at
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

@app.route('/publicaciones')
def publicaciones():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM publicaciones ORDER BY created_at DESC")
    publications = cursor.fetchall()
    return render_template('publicaciones.html', publications=publications)

if __name__ == '__main__':
    app.run(debug=True)
