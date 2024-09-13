# Archivo para manejar el sistema de autenticacion

# Librerias y modulos
from flask import Flask, render_template, request, redirect, url_for, flash
from models.autenticacionModel import register_user, check_login
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Funcion para registrar una nueva cuenta
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['register-nombre']
        correo = request.form['register-correo']
        contrasenia = request.form['register-password']
        confirmar_contrasenia = request.form['register-confirm-password']

# Validar que confirmar contrasenia sea igual a contrasenia
        if contrasenia != confirmar_contrasenia:
            flash("Las contraseñas no coinciden")
            return render_template('autenticacion.html')

# Si el correo ya existe retornar a la interfaz del Login
        user_exists = check_login(correo, contrasenia)
        if user_exists:
            flash("El correo ya está registrado", "error")
            return render_template('autenticacion.html')
        else:
            # Si todos los datos estan correctos mostrar un mensaje de exito
            register_user(nombre, correo, contrasenia)
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('login'))

        # Plantilla de HTML para manejar la parte de autenticacion de usuario
        return render_template('autenticacion.html')


# Funcion para iniciar sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['login-correo']
        contrasenia = request.form['login-password']
        user = check_login(correo, contrasenia)

        if user:
            # Si las credenciales son correctas redirigir a la siguiente pagina
            next_page = request.form.get('next')
            print(f"DEBUG: next_page = {next_page}")

            # Revisar si la siguiente pagina corresponde a la interfaz de las campanias
            if next_page == 'campaniaForm':
                return redirect(url_for('campanias', form_type=next_page))
            else:
                # Si no corresponde  las campanias redirigir a la interfaz del foro
                return redirect(url_for('foro', form_type=next_page))
        else:
            # Si las credenciales no son correctas mostrar un mensaje de error y mantener al usuario en la misma pagina
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
