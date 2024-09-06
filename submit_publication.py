# Este archivo no esta funcionando ya que el metodo se implemento directamente en el archivo
# publicaciones.py

from flask import Flask, render_template, request, redirect, url_for, flash
from db import create_connection

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit_publication', methods=['GET', 'POST'])
def submit_publication():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        image_file = request.files.get('image')

        if title and category and content:
            image_data = None
            if image_file and allowed_file(image_file.filename):
                # Lee el archivo como Binario
                image_data = image_file.read()

            # Save the publication in the database
            connection = create_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO Publicaciones (title, category, content, image_data)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (title, category, content, image_data))
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
