# Archivo para manejar la logica de las publicaciones patrocinadas

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from config import Config
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

# Configuraciones del mail server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Para que pueda funcionar estas credenciales
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Tienen que ser correctas, en este caso estoy dejando sample data

# Sin embrago el archivo siempre se va guardar en la carpeta Uploads

app.config['UPLOAD_FOLDER'] = 'uploads/'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mail = Mail(app)

# Definicion de la ruta para patrocinar publicacion
@app.route('/pp', methods=['GET', 'POST'])
def pp():
    if request.method == 'POST':
        titulo = request.form['titulo']
        correo = request.form['correo']
        telefono = request.form['telefono']
        donativo = request.form['donativo']
        categoria = request.form['categoria']
        organizacion = request.form['organizacion']

        # Maneja cuando se suban archivos
        if 'contenido' not in request.files:
            flash('No se ha subido ningún archivo.')
            return redirect(request.url)

        file = request.files['contenido']
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)


            msg = Message('Nueva solicitud de patrocinio',
                          sender='your_email@gmail.com',
                          recipients=['elmerurbina570@gmail.com'])
            msg.body = f'''
            Título de la publicación: {titulo}
            Correo: {correo}
            Número de teléfono: {telefono}
            Donativo: ${donativo}
            Categoría: {categoria}
            Organización: {organizacion}
            '''
            with app.open_resource(filepath) as fp:
                msg.attach(filename, file.content_type, fp.read())
            mail.send(msg)

            flash('Su publicación se ha enviado con éxito, pronto recibirá instrucciones de nuestro equipo.')
            return redirect(url_for('solicitud'))
        else:
            flash('Tipo de archivo no permitido. Por favor sube un archivo PDF o DOCX.')
            return redirect(request.url)

    return render_template('patrocinarPublicacion.html')

# Solo permiten archivos con extension pdf y docx
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

if __name__ == '__main__':
    app.run(debug=True)
