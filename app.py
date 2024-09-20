# Archivo principal para manejar todas las rutas

# Importacion de librerias y modulos
from flask import Flask, render_template
from  flask_login import LoginManager
from controllers.autenticacion import register, login, nuevasCredenciales, recuperarCuenta
from controllers.publicaciones import publicaciones
from controllers.campanias import campanias, new_campaign, add_comment
from controllers.denuncia import denuncia, denunciaForm, submit_denuncia
from controllers.foro import (
    foro, new_debate, edit_debate, edit_question,
    delete_debate_route, new_question,
    delete_question_route, new_thread, respuestas,
    edit_thread, new_response, delete_thread_route
)
from models.foroModel import get_all_debates, get_all_questions, get_all_threads, get_question_by_id, get_debate_by_id, get_thread_by_id

from settings import Config
from controllers.submit_publication import submit_publication, dislike_publication, like_publication
from controllers.ia import recognize
from controllers.PatrocinarPublicacion import pp
from models.autenticacionModel import User
from controllers.profileController import profile, edit_profile, delete_profile, logout, unauthorized


# Inicializacion de la aplicacion Flask
app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)

# Definir la función de carga de usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



# Ruta del Index
@app.route('/verdeNica')
def verdeNica():
    return render_template('index.html')

# Ruta de la interfaz de empresas sostenibles
@app.route('/ep')
def ep():
    return render_template('empresasSostenibles.html')

# Ruta de la interfaz de Biodiversidad en Nicaragua
@app.route('/biodiversidad')
def biodiversidad():
    return render_template('biodiversidad.html')

@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401


app.add_url_rule('/profile', 'profile', profile)
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/edit_profile', 'edit_profile', edit_profile, methods=['GET', 'POST'])
app.add_url_rule('/delete_profile', 'delete_profile', delete_profile, methods=['POST'])


# Rutas del sistema de autenticacion
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/recuperarCuenta', 'recuperarCuenta', recuperarCuenta)
app.add_url_rule('/nuevasCredenciales', 'nuevasCredenciales', nuevasCredenciales)

# Rutas para las interfaces del Foro
app.add_url_rule('/campanias', 'campanias', campanias)
app.add_url_rule('/new_campaign', 'new_campaign', new_campaign, methods=['POST'])
app.add_url_rule('/add_comment', 'add_comment', add_comment, methods=['POST'])

# Ruta para la parte de las publicaciones
app.add_url_rule('/submit_publication', 'submit_publication', submit_publication, methods=['GET', 'POST'])
app.add_url_rule('/publicaciones', 'publicaciones', publicaciones)
app.add_url_rule('/like/<int:publication_id>', 'like_publication', like_publication, methods=['POST'])
app.add_url_rule('/dislike/<int:publication_id>', 'dislike_publication', dislike_publication, methods=['POST'])


# Ruta de la parte de las denuncias
app.add_url_rule('/denuncia', 'denuncia', denuncia) # Mostrar las denuncias
app.add_url_rule('/denunciaForm', 'denunciaForm', denunciaForm) # Formulario
app.add_url_rule('/submit_denuncia', 'submit_denuncia', submit_denuncia, methods=['POST']) # Enviar denuncia

app.add_url_rule('/foro', 'foro', foro)

# Ruta para agregar un nuevo debate
app.add_url_rule('/new_debate', 'new_debate', new_debate, methods=['POST'])

# Ruta para editar un debate
app.add_url_rule('/edit_debate/<int:debate_id>', 'edit_debate', edit_debate, methods=['GET', 'POST'])

# Ruta para eliminar un debate
app.add_url_rule('/delete_debate/<int:debate_id>', 'delete_debate_route', delete_debate_route, methods=['POST'])

# Rutas para preguntas
app.add_url_rule('/new_question', 'new_question', new_question, methods=['POST'])
app.add_url_rule('/edit_question/<int:question_id>', 'edit_question', edit_question, methods=['GET', 'POST'])
app.add_url_rule('/delete_question/<int:question_id>', 'delete_question_route', delete_question_route, methods=['POST'])

# Rutas para hilos de conversación
app.add_url_rule('/new_thread', 'new_thread', new_thread, methods=['POST'])
app.add_url_rule('/edit_thread/<int:thread_id>', 'edit_thread', edit_thread, methods=['GET', 'POST'])
app.add_url_rule('/delete_thread/<int:thread_id>', 'delete_thread_route', delete_thread_route, methods=['POST'])

# Ruta para mostrar el perfil de usuario
app.add_url_rule('/profile', 'profile', profile)

# Nueva respuesta
app.add_url_rule('/new_response', 'new_response', new_response, methods=['POST'])

# Ruta para la interfaz de las respuestas
app.add_url_rule('/respuestas', 'respuestas', respuestas)

app.add_url_rule('/get_all_debates', 'get_all_debates', get_all_debates())
app.add_url_rule('/get_all_questions', 'get_all_questions', get_all_questions())
app.add_url_rule('/get_all_threads', 'get_all_threads', get_all_threads())
app.add_url_rule('/get_debate_by_id/<int:debate_id>', 'get_debate_by_id', get_debate_by_id)
app.add_url_rule('/get_question_by_id/<int:question_id>', 'get_question_by_id', get_question_by_id)
app.add_url_rule('/get_thread_by_id/<int:thread_id>', 'get_thread_by_id', get_thread_by_id)

app.add_url_rule('/pp','pp', pp, methods=['GET', 'POST'])


# Interfaz del modelo de Inteligencia Artificial
@app.route('/ia', methods=['GET'])
def ia():
    return render_template('ia.html')


# Parte del sistema de IA para reconocimiento de especies animales/plantas mediante imagen
app.add_url_rule('/recognize', 'recognize', recognize, methods=['POST'])


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
