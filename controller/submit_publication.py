from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from settings import Config, create_connection

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def like_publication(publication_id):
    connection = create_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE Publicaciones
    SET likes = likes + 1
    WHERE id = %s
    """
    cursor.execute(update_query, (publication_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(success=True)

# Dislike Publication method
def dislike_publication(publication_id):
    connection = create_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE Publicaciones
    SET dislikes = dislikes + 1
    WHERE id = %s
    """
    cursor.execute(update_query, (publication_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(success=True)

@app.route('/submit_publication', methods=['GET', 'POST'])
def submit_publication():
    """Handle publication submission and image upload."""
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        image_file = request.files.get('image')

        if title and category and content:
            image_filename = None
            if image_file and allowed_file(image_file.filename):
                # Save the file
                image_filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            # Save the publication in the database
            connection = create_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO Publicaciones (title, category, content, image_filename)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (title, category, content, image_filename))
            connection.commit()

            cursor.close()
            connection.close()

            flash('Publicación creada con éxito', 'success')
            return redirect(url_for('submit_publication'))
        else:
            flash('Por favor, completa todos los campos requeridos.', 'danger')
            return render_template('new_publication.html')

    # Render the form for GET requests
    return render_template('new_publication.html')

if __name__ == '__main__':
    app.run(debug=True)
