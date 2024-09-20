from flask import render_template, request, redirect, url_for, flash, Flask
from flask_login import login_required, current_user, LoginManager, login_user
from flask_login import logout_user
from models.profileModel import update_profile, delete_user
from werkzeug.security import generate_password_hash
from settings import Config
from models.autenticacionModel import User

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'

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

# Route to display the profile edit form
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasenia = request.form.get('contrasenia')

        # Check if all fields are provided
        if not nombre or not correo:
            flash('El nombre y el correo electrónico son obligatorios.', 'error')
            return redirect(url_for('edit_profile'))

        # If password is provided, hash it before updating
        hashed_password = None
        if contrasenia:
            hashed_password = generate_password_hash(contrasenia)

        # Update the profile in the database
        success = update_profile(current_user.id, nombre, correo, hashed_password)
        if success:
            flash('Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Hubo un error al actualizar el perfil.', 'error')

    # Render the edit profile template
    return render_template('edit_profile.html', user=current_user)


# Route to delete the user's profile
@app.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    user_id = current_user.id

    # Delete the user from the database
    success = delete_user(user_id)
    if success:
        flash('Perfil eliminado exitosamente.', 'success')
        # Optionally redirect to a logout route after deleting the profile
        return redirect(url_for('logout'))
    else:
        flash('Hubo un error al eliminar el perfil.', 'error')
        return redirect(url_for('profile'))
