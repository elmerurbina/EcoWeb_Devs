import os
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from models.denounces_model import save_denuncia, get_all_denuncias
from settings import Config


class DenounceApp:
    """Class to handle the logic for denounces"""

    def __init__(self):
        """Initialize the application and configuration"""
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = 'static/uploads'
        self.app.config.from_object(Config)

        # Check if the upload directory exists, create if not
        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

        # Allowed file extensions for uploads
        self.ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx', 'mp4', 'mp3'}

        # Register routes
        self.app.add_url_rule('/denounce', view_func=self.denounce)
        self.app.add_url_rule('/denounce_form', view_func=self.denounce_form)
        self.app.add_url_rule('/submit_denuncia',
                              view_func=self.submit_denuncia, methods=['POST'])

    def allowed_file(self, filename):
        """Check if the file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def denounce(self):
        """Route to display all denounces"""
        denuncias = get_all_denuncias()
        return render_template('denounces.html', denuncias=denuncias)

    def denounce_form(self):
        """Route to display the denounce submission form"""
        return render_template('denounces_form.html')

    def submit_denuncia(self):
        """Handle the submission of a new denounce"""
        if request.method == 'POST':
            # Fetch form data
            titulo = request.form.get('titulo', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            ubicacion = request.form.get('ubicacion', '').strip()
            denunciados = request.form.get('denunciados', '').strip()
            otros_detalles = request.form.get('otros_detalles', '').strip()

            # Validate required fields
            if not titulo or not descripcion or not ubicacion:
                flash('All required fields must be completed.', 'error')
                return redirect(url_for('denounce_form'))

            filename = None

            # Handle evidence file upload
            if 'evidencia' in request.files:
                evidencia_file = request.files['evidencia']

                if evidencia_file.filename == '':
                    flash('You must attach evidence.', 'error')
                    return redirect(url_for('denounce_form'))

                if evidencia_file and self.allowed_file(evidencia_file.filename):
                    filename = secure_filename(evidencia_file.filename)
                    (evidencia_file.save
                     (os.path.join(self.app.config['UPLOAD_FOLDER'], filename)))
                    flash('File successfully uploaded', 'success')
                else:
                    flash('Invalid file format', 'warning')
                    return redirect(url_for('denounce_form'))

            # Save the submitted denounce in the database
            try:
                save_denuncia(titulo, descripcion,
                              filename, ubicacion, denunciados, otros_detalles)
                flash('Denounce saved successfully', 'success')
            except Exception as e:
                flash(f'Error saving denounce: {str(e)}', 'error')

            return redirect(url_for('denounce'))

    def run(self):
        """Run the Flask app"""
        self.app.run(debug=True)


if __name__ == '__main__':
    # Create an instance of the DenounceApp class and run the app
    app_instance = DenounceApp()
    app_instance.run()
