# Main file to manage all the routes
# Packages and modules import
from flask import Flask, render_template
from flask_login import LoginManager
from controllers.authentication_controller import (
    register, login,nuevasCredenciales, recuperarCuenta)
from controllers.publications_controller import publicaciones
from controllers.campaigns_controller import campanias, new_campaign, add_comment
from controllers.denounce_controller import denuncia, denunciaForm, submit_denuncia
from controllers.forum_controller import (
    foro, new_debate, edit_debate, edit_question,
    delete_debate_route, new_question,
    delete_question_route, new_thread, respuestas,
    edit_thread, new_response, delete_thread_route
)
from settings import Config
from controllers.submit_publicationController import (
    submit_publication, dislike_publication, like_publication)
from controllers.ai_controller import recognize
from controllers.sponsor_publicationController import pp
from controllers.profile_controller import (
    profile, edit_profile, delete_profile, logout)
from models.forum_model import (
    get_all_debates, get_all_questions, get_all_threads,
    get_question_by_id,get_debate_by_id, get_thread_by_id
)
from models.authentication_model import User


# Flask application initialization
app = Flask(__name__)
# Used for load the secret key
app.config.from_object(Config)
# Call the login manager function
login_manager = LoginManager()
# Initialize the application of with the login manager
login_manager.init_app(app)


# Function to load the user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Show a personalized page when sesion has expired
@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401


# Route of the main page
@app.route('/verdeNica')
def verdeNica():
    return render_template('index.html')


# Routes to manage the user's profile
app.add_url_rule('/profile', 'profile', profile)
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/edit_profile', 'edit_profile',
                 edit_profile, methods=['GET', 'POST'])
app.add_url_rule('/delete_profile', 'delete_profile',
                 delete_profile, methods=['POST'])


# Routes to manage the authentication system
app.add_url_rule('/register', 'register',
                 register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login',
                 login, methods=['GET', 'POST'])
app.add_url_rule('/recuperarCuenta',
                 'recuperarCuenta', recuperarCuenta)
app.add_url_rule('/nuevasCredenciales',
                 'nuevasCredenciales', nuevasCredenciales)


# Routes for Campaigns management
app.add_url_rule('/campanias', 'campanias', campanias)
app.add_url_rule('/new_campaign', 'new_campaign',
                 new_campaign, methods=['POST'])
app.add_url_rule('/add_comment', 'add_comment',
                 add_comment, methods=['POST'])

# Routes to manage the publications
app.add_url_rule('/submit_publication', 'submit_publication',
                 submit_publication, methods=['GET', 'POST'])
app.add_url_rule('/publicaciones', 'publicaciones', publicaciones)
# Get the user id when someone like or dislike a publication
app.add_url_rule('/like/<int:publication_id>',
                 'like_publication', like_publication, methods=['POST'])
app.add_url_rule('/dislike/<int:publication_id>',
                 'dislike_publication', dislike_publication,
                 methods=['POST'])


# Routes to manage the denounces interfaces
app.add_url_rule('/denuncia', 'denuncia', denuncia)
app.add_url_rule('/denunciaForm', 'denunciaForm', denunciaForm)
app.add_url_rule('/submit_denuncia', 'submit_denuncia',
                 submit_denuncia, methods=['POST'])


''' 
    The section of the Forum is divided in three categories:
    Debates: which is intended for opinions in a specific topic.
    Questions: Intended for creating specific questions.
    Thread: Is to people who want to talk openly about a topic.
'''
# Main template of the forum
app.add_url_rule('/foro', 'foro', foro)
# Route to add a new debate
app.add_url_rule('/new_debate', 'new_debate', new_debate, methods=['POST'])
# Route to edit a debate
app.add_url_rule('/edit_debate/<int:debate_id>', 'edit_debate',
                 edit_debate, methods=['GET', 'POST'])
# Route to delete debate
app.add_url_rule('/delete_debate/<int:debate_id>',
                 'delete_debate_route', delete_debate_route, methods=['POST'])
'''
    The next three routes are for creating,
    editing and deleting a question.
'''
app.add_url_rule('/new_question', 'new_question',
                 new_question, methods=['POST'])
app.add_url_rule('/edit_question/<int:question_id>',
                 'edit_question', edit_question, methods=['GET', 'POST'])
app.add_url_rule('/delete_question/<int:question_id>',
                 'delete_question_route', delete_question_route,
                 methods=['POST'])
'''
    The next three routes are for creating,
    editing and deleting a conversation thread.
'''
app.add_url_rule('/new_thread', 'new_thread',
                 new_thread, methods=['POST'])
app.add_url_rule('/edit_thread/<int:thread_id>',
                 'edit_thread', edit_thread,
                 methods=['GET', 'POST'])
app.add_url_rule('/delete_thread/<int:thread_id>',
                 'delete_thread_route',
                 delete_thread_route, methods=['POST'])
# Route to add a new response or answer
app.add_url_rule('/new_response', 'new_response',
                 new_response, methods=['POST'])
# Route to see the existing answers
app.add_url_rule('/respuestas', 'respuestas', respuestas)
'''
    The next three routes are to get all the debates, questions,
    and threads from the database and display them on the main template.
'''
app.add_url_rule('/get_all_debates',
                 'get_all_debates', get_all_debates())
app.add_url_rule('/get_all_questions',
                 'get_all_questions', get_all_questions())
app.add_url_rule('/get_all_threads',
                 'get_all_threads', get_all_threads())
''' 
    The next three routes are for getting the forum content,
    based on the id to associate it with an answer when it's added.
'''
app.add_url_rule('/get_debate_by_id/<int:debate_id>',
                 'get_debate_by_id', get_debate_by_id)
app.add_url_rule('/get_question_by_id/<int:question_id>',
                 'get_question_by_id', get_question_by_id)
app.add_url_rule('/get_thread_by_id/<int:thread_id>',
                 'get_thread_by_id', get_thread_by_id)


'''
This route is the template to loading the sustainable products.
pp stands for 'producto sostenible'
'''
app.add_url_rule('/pp','pp', pp, methods=['GET', 'POST'])


# This function is for the Artificial intelligence model
@app.route('/ia', methods=['GET'])
def ia():
    return render_template('ia.html')
# Function to recognize a specie based on an image uploaded
app.add_url_rule('/recognize', 'recognize', recognize, methods=['POST'])


# Ruta de la interfaz de empresas sostenibles
@app.route('/ps')
def ps():
    return render_template('productosSostenibles.html')


@app.route('/documentacion')
def documentacion():
    return render_template('05Manual_de_uso.html')


# Ruta de la interfaz de Biodiversidad en Nicaragua
@app.route('/biodiversidad')
def biodiversidad():
    return render_template('biodiversidad.html')




             # RUTAS INDEPENDIENTES PARA LAS PAGINAS DE PUBLICACIONES SEPARADAS

@app.route('/deforestacion')
def deforestacion():
    return render_template('deforestacion.html')

@app.route('/gei')
def gei():
    return render_template('GEI.html')

@app.route('/cf')
def cf():
    return render_template('cf.html')

@app.route('/dcp')
def dcp():
    return render_template('DCP.html')

@app.route('/anm')
def anm():
    return render_template('ANM.html')


@app.route('/alpp')
def alpp():
    return render_template('alpp.html')

@app.route('/sequias')
def sequias():
    return render_template('sequias.html')

@app.route('/inundaciones')
def inundaciones():
    return render_template('inundaciones.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/sostenibilidad')
def sostenibilidad():
    return render_template('sostenibilidad.html')

@app.route('/rs')
def rs():
    return render_template('recursosNaturales.html')

@app.route('/energiasRenovable')
def energiasRenovables():
    return render_template('energiaRenovable.html')

@app.route('/eficienciaEnergetica')
def eficienciaEnergetica():
    return render_template('eficienciaEnergetica.html')

@app.route('/transporteSostenible')
def transporteSostenible():
    return render_template('transporteSostenible.html')

@app.route('/agriculturaSostenible')
def agriculturaSostenible():
    return render_template('agricultura.html')

@app.route('/ecosistemas')
def ecosistemas():
    return render_template('ecosistemas.html')

@app.route('/dietasSostenibles')
def dietasSostenibles():
    return render_template('dietasSostenible.html')

@app.route('/reciclaje')
def reciclaje():
    return render_template('reciclaje.html')

@app.route('/politicasAmbientales')
def politicasAmbientales():
    return render_template('politicasAmbientales.html')

@app.route('/tecnologias')
def tecnologias():
    return render_template('tecnologia.html')

@app.route('/concienciaPublica')
def concienciaPublica():
    return render_template('concienciaPublica.html')

if __name__ == '__main__':
    app.run(debug=True)
