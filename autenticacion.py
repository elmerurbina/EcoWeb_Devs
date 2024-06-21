from flask import Flask, render_template, request, redirect, url_for, flash
from db import register_user, check_login
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


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
        else:
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
            print(f"DEBUG: next_page = {next_page}")  # Debug statement
            return redirect(url_for('foro', form_type=next_page))
        else:
            flash("Correo o contraseña incorrecta")
            return render_template('autenticacion.html', next=request.form.get('next', ''))
    return render_template('autenticacion.html', next=request.args.get('next', ''))


if __name__ == '__main__':
    app.run(debug=True)
