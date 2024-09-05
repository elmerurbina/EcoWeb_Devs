import os
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from db import save_denuncia, get_all_denuncias

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx', 'mp4', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Necessary for flashing messages

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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit_denuncia', methods=['POST'])
def submit_denuncia():
    if request.method == 'POST':
        # Fetch form data
        titulo = request.form.get('titulo', '')
        descripcion = request.form.get('descripcion', '')
        ubicacion = request.form.get('ubicacion', '')
        denunciados = request.form.get('denunciados', '')
        otros_detalles = request.form.get('otros_detalles', '')

        filename = None

        # Manejo de los archivos de la evidencia
        if 'evidencia' in request.files:
            evidencia_file = request.files['evidencia']

            if evidencia_file and allowed_file(evidencia_file.filename):
                filename = secure_filename(evidencia_file.filename)
                evidencia_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Archivo agregado con éxito', 'success')
            else:
                flash('Archivo no válido o no se proporcionó archivo', 'warning')

        # Save denuncia data to database
        try:
            save_denuncia(titulo, descripcion, filename, ubicacion, denunciados, otros_detalles)
            flash('Denuncia guardada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al guardar la denuncia: {str(e)}', 'error')

        return redirect(url_for('denuncia'))

if __name__ == '__main__':
    app.run(debug=True)
