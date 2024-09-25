import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models.profile_model import update_profile, delete_user
from settings import Config, create_connection
from mysql.connector import Error
from models.authentication_model import User


app = Flask(__name__)
app.config.from_object(Config)

# Configure file upload settings
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder where uploaded files will be saved
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB


@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.unauthorized_handler = unauthorized

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Profile route (requires login)
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasenia = request.form.get('contrasenia')

        # Check if name and email are provided
        if not nombre or not correo:
            flash('El nombre y el correo electrónico son obligatorios.', 'error')
            return redirect(url_for('edit_profile'))

        # Handle password: hash it if provided, else set to None
        hashed_password = generate_password_hash(contrasenia) if contrasenia else None

        # Handle profile photo upload
        photo = request.files.get('profile_photo')
        if photo and photo.filename:  # If an image is uploaded
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_photo_url = os.path.join('uploads', filename)
        else:  # No new image uploaded, retain the existing one
            profile_photo_url = current_user.profile_photo

        # Update the profile in the database
        success = update_profile(current_user.id, nombre, correo, hashed_password, profile_photo_url)
        if success:
            flash('Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Hubo un error al actualizar el perfil.', 'error')

    return render_template('edit_profile.html', user=current_user)

def update_profile(user_id, nombre, correo, hashed_password, profile_photo_url):
    # Implement the logic to update the user profile in the database.
    # Make sure to check if hashed_password is None, and update accordingly.
    connection = create_connection()
    cursor = connection.cursor()
    try:
        query = "UPDATE sistemaautenticacion SET nombre=%s, correo=%s, profile_photo=%s"
        params = [nombre, correo, profile_photo_url]

        if hashed_password:  # Update password only if provided
            query += ", contrasenia=%s"
            params.append(hashed_password)

        query += " WHERE id=%s"
        params.append(user_id)

        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Route to delete the user's profile
@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    user_id = current_user.id

    # Delete the user from the database
    success = delete_user(user_id)
    if success:
        flash('Perfil eliminado exitosamente.', 'success')
        return redirect(url_for('logout'))
    else:
        flash('Hubo un error al eliminar el perfil.', 'error')
        return redirect(url_for('profile'))
