# Archivo para manejar la logica de las denuncias

# Importacion de Modulos y librerias
import os
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from models.denounces_model import save_denuncia, get_all_denuncias
from settings import Config

# Guardar las fotos subidas en el folder uploads dentro de la carpeta static
UPLOAD_FOLDER = 'static/uploads'

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx', 'mp4', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)

# Comprobar que el directorio para uploads es correcto
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta para la interfaz principal de las denuncias
@app.route('/denounce')
def denounce():
    # Obtener todas las denuncias desde la base de datos
    denuncias = get_all_denuncias()
    return render_template('denounces.html', denuncias=denuncias)

# Ruta para la interfaz del formulario de las denuncias
@app.route('/denounce_form')
def denounce_form():
    return render_template('denounces_form.html')

# Comprobar que el archivo está dentro de las extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Funcion para guardar las denuncias
@app.route('/submit_denuncia', methods=['POST'])
def submit_denuncia():
    if request.method == 'POST':
        # Fetch form data
        titulo = request.form.get('titulo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        ubicacion = request.form.get('ubicacion', '').strip()
        denunciados = request.form.get('denunciados', '').strip()
        otros_detalles = request.form.get('otros_detalles', '').strip()

        # Revisar que todos los campos requeridos esten llenados
        if not titulo or not descripcion or not ubicacion:
            flash('Todos los campos obligatorios deben ser completados.', 'error')
            return redirect(url_for('denunciaForm'))

        filename = None

        # Manejo de los archivos de la evidencia
        if 'evidencia' in request.files:
            evidencia_file = request.files['evidencia']

            if evidencia_file.filename == '':
                flash('Debes adjuntar una evidencia.', 'error')
                return redirect(url_for('denunciaForm'))

            if evidencia_file and allowed_file(evidencia_file.filename):
                filename = secure_filename(evidencia_file.filename)
                evidencia_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Archivo agregado con éxito', 'success')
            else:
                flash('Archivo no válido', 'warning')
                return redirect(url_for('denunciaForm'))

        # Guardar la denuncia en la base de datos
        try:
            save_denuncia(titulo, descripcion, filename, ubicacion, denunciados, otros_detalles)
            flash('Denuncia guardada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al guardar la denuncia: {str(e)}', 'error')

        return redirect(url_for('denuncia'))

if __name__ == '__main__':
    app.run(debug=True)
