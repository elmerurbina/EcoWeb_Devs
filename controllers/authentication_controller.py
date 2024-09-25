# authentication_controller.py
from flask import render_template, request, redirect, url_for, flash, Flask
from flask_login import login_user
from models.authentication_model import register_user, check_login, User
from settings import Config


class AuthenticationController:
    def __init__(self, app):
        self.app = app
        self.app.config.from_object(Config)

        # Register routes
        self.app.route('/register', methods=['GET', 'POST'])(self.register)
        self.app.route('/login', methods=['GET', 'POST'])(self.login)
        self.app.route('/campaign', methods=['GET'])(self.campaign)
        self.app.route('/recover_account', methods=['GET'])(self.recover_account)
        self.app.route('/new_credentials', methods=['GET'])(self.new_credentials)

    def register(self):
        """Handles user registration."""
        if request.method == 'POST':
            name = request.form['register-nombre']
            email = request.form['register-correo']
            password = request.form['register-password']
            confirm_password = request.form['register-confirm-password']

            # Validate that confirm password is the same as password
            if password != confirm_password:
                flash("Las contraseñas no coinciden")
                return render_template('authentication.html')

            # Check if the email already exists
            user_exists = check_login(email, password)
            if user_exists:
                flash("El correo ya está registrado", "error")
                return render_template('authentication.html')
            else:
                # If all data is correct, show a success message
                register_user(name, email, password)
                flash("Usuario registrado exitosamente", "success")
                return redirect(url_for('login'))

        return render_template('authentication.html')

    def login(self):
        """Handles user login."""
        if request.method == 'POST':
            email = request.form['login-correo']
            password = request.form['login-password']
            remember_me = 'remember_me' in request.form  # Check if "Remember Me" checkbox is checked

            # Check login credentials (ensure this function checks email and password)
            user_data = check_login(email, password)

            if user_data:
                # Create User instance with the required fields (id, name, email, password, profile_photo)
                user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])

                # Log in the user, passing remember=True if the checkbox is checked
                login_user(user, remember=remember_me)

                # Handle the redirect to the next page or default to the profile/forum
                next_page = request.form.get('next')
                print(f"DEBUG: next_page = {next_page}")  # Debugging output

                if next_page == 'profile':
                    return redirect(url_for('profile'))  # Redirect to profile route
                elif next_page == 'campaniaForm':
                    return redirect(url_for('campaign', form_type=next_page))
                else:
                    return redirect(url_for('forum', form_type=next_page))  # Default to forum

            else:
                # If login fails, show an error message
                flash("Correo o contraseña incorrecta", "error")
                return render_template('authentication.html', next=request.form.get('next', ''))

        # If the method is GET, render the authentication form
        return render_template('authentication.html', next=request.args.get('next', ''))

    def campaign(self):
        """Renders the campaign interface."""
        form_type = request.args.get('form_type', '')
        return render_template('campaigns.html', form_type=form_type)

    def recover_account(self):
        """Renders the account recovery interface."""
        return render_template('recover_account.html')

    def new_credentials(self):
        """Renders the new credentials interface."""
        return render_template('new_credentials.html')


if __name__ == '__main__':
    app = Flask(__name__)
    authentication_controller = AuthenticationController(app)
    app.run(debug=True)
