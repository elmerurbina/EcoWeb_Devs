from flask import Flask, render_template, request, redirect, url_for, flash
from db import register_user, check_login

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['register-nombre']
        correo = request.form['register-correo']
        contrasenia = request.form['register-password']
        confirmar_contrasenia = request.form['register-confirm-password']

        if contrasenia != confirmar_contrasenia:
            flash("Las contraseñas no coinciden")
            return render_template('autenticacion.html')

        user_exists = check_login(correo, contrasenia)
        if user_exists:
            flash("El correo ya está registrado")
            return render_template('autenticacion.html')

        register_user(nombre, correo, contrasenia)
        flash("Usuario registrado exitosamente")
        return redirect(url_for('login'))
    return render_template('autenticacion.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['login-correo']
        contrasenia = request.form['login-password']
        user = check_login(correo, contrasenia)

        if user:
            next_page = request.form.get('next')
            if next_page == 'campanias':
                return redirect(url_for('campanias'))
            elif next_page == 'foro':
                return redirect(url_for('foro'))
            else:
                return redirect(url_for('index'))
        else:
            flash("Correo o contraseña incorrecta")
            return render_template('autenticacion.html')
    return render_template('autenticacion.html')


@app.route('/cs')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
