# autenticacion.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask
from flask_login import login_user
from models.autenticacionModel import register_user, check_login, User
from settings import Config


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['register-nombre']
        correo = request.form['register-correo']
        contrasenia = request.form['register-password']
        confirmar_contrasenia = request.form['register-confirm-password']

        # Validate that confirm password is the same as password
        if contrasenia != confirmar_contrasenia:
            flash("Las contraseñas no coinciden")
            return render_template('autenticacion.html')

        # Check if the email already exists
        user_exists = check_login(correo, contrasenia)
        if user_exists:
            flash("El correo ya está registrado", "error")
            return render_template('autenticacion.html')
        else:
            # If all data is correct, show a success message
            register_user(nombre, correo, contrasenia)
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('login'))

    return render_template('autenticacion.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['login-correo']
        contrasenia = request.form['login-password']
        user_data = check_login(correo, contrasenia)  # Ensure this returns necessary data

        if user_data:
            # Create User instance with id, nombre, correo, contrasenia, and profile_photo
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])  # user_data[0] is id, [1] is nombre, [2] is correo, [3] is contrasenia, [4] is profile_photo

            # Log in the user
            login_user(user)

            # Redirect to the next page or to profile if no next page is specified
            next_page = request.form.get('next')
            print(f"DEBUG: next_page = {next_page}")  # Debugging output

            if next_page == 'profile':
                return redirect(url_for('profile'))  # Redirect to profile route
            elif next_page == 'campaniaForm':
                return redirect(url_for('campanias', form_type=next_page))
            else:
                return redirect(url_for('foro', form_type=next_page))  # Default to foro

        else:
            flash("Correo o contraseña incorrecta", "error")
            return render_template('autenticacion.html', next=request.form.get('next', ''))

    return render_template('autenticacion.html', next=request.args.get('next', ''))


# Ruta para la interfaz de las campanias
@app.route('/campania')
def campania():
    form_type = request.args.get('form_type', '')
    return render_template('campania.html', form_type=form_type)

# Ruta para la interfaz de recuperacion de cuenta
@app.route('/recuperarCuenta')
def recuperarCuenta():
    return render_template('recuperarCuenta.html')


# Ruta para ingresar las nuevas redenciales
@app.route('/nuevasCredenciales')
def nuevasCredenciales():
    return render_template('nuevasCredenciales.html')

if __name__ == '__main__':
    app.run(debug=True)
