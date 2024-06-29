import os
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from db import save_denuncia, get_all_denuncias

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx', 'mp4', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/denuncia')
def denuncia():
    denuncias = get_all_denuncias()
    return render_template('denuncia.html', denuncias=denuncias)

@app.route('/denunciaForm')
def denunciaForm():
    return render_template('denunciaForm.html')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx', 'mp4', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Funcion para revisar los formatos permitidos
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for submitting denuncia form
@app.route('/submit_denuncia', methods=['POST'])
def submit_denuncia():
    if request.method == 'POST':
        # Fetch form data
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        ubicacion = request.form['ubicacion']
        denunciados = request.form['denunciados']
        otros_detalles = request.form.get('otros_detalles', '')  # Optional field

        # Handle file upload for evidencia
        if 'evidencia' not in request.files:
            flash('No se proporciono ningun archivo')
            return redirect(request.url)

        evidencia_file = request.files['evidencia']

        if evidencia_file.filename == '':
            flash('No hay archivos seleccionado')
            return redirect(request.url)

        if evidencia_file and allowed_file(evidencia_file.filename):
            filename = secure_filename(evidencia_file.filename)
            evidencia_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Archivo agregado con exito')
        else:
            flash('Archivo no valido')
            return redirect(request.url)

        # Save denuncia data to database
        try:
            save_denuncia(titulo, descripcion, filename, ubicacion, denunciados, otros_detalles)
            flash('Denuncia guardada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al guardar la denuncia: {str(e)}', 'error')

        return redirect(url_for('denuncia'))



if __name__ == '__main__':
    app.run(debug=True)