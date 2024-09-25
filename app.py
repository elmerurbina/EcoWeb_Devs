# Main file to manage all the routes
# Packages and modules import
from flask import Flask, render_template
from flask_login import LoginManager, login_required
from datetime import timedelta
from controllers.authentication_controller import AuthenticationController
from controllers.publications_controller import publications
from controllers.campaigns_controller import campaigns, new_campaign, add_comment
from controllers.denounce_controller import DenounceApp
from controllers.forum_controller import ForumController
from settings import Config
from controllers.submit_publication_controller import (
    submit_publication, dislike_publication, like_publication)
from controllers.ai_controller import  recognize
from controllers.sponsor_publication_controller import pp
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
# Instantiate the AuthenticationController
auth_controller = AuthenticationController(app)
# Users will be remembered for 30 days
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

# AI Model recognition routes
app.add_url_rule('/recognize', 'recognize', recognize, methods=['POST'])
# Load the main template for the ai model
@app.route('/ia', methods=['GET'])
def ia():
    return render_template('ai.html')

# Function to load the user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Show a personalized page when session has expired
@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401


# Route of the main page
@app.route('/verde_nica')
def verde_nica():
    return render_template('index.html')


# Routes to manage the user's profile
app.add_url_rule('/profile', 'profile', profile)
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/edit_profile', 'edit_profile',
                 edit_profile, methods=['GET', 'POST'])
app.add_url_rule('/delete_profile', 'delete_profile',
                 delete_profile, methods=['POST'])

# Routes to manage the authentication system
app.add_url_rule('/register', 'register', auth_controller.register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', auth_controller.login, methods=['GET', 'POST'])
app.add_url_rule('/campaign', 'campaign', auth_controller.campaign, methods=['GET'])
app.add_url_rule('/recover_account', 'recover_account', auth_controller.recover_account, methods=['GET'])
app.add_url_rule('/new_credentials', 'new_credentials', auth_controller.new_credentials, methods=['GET'])


# Routes for Campaigns management
app.add_url_rule('/campaigns', 'campaigns', campaigns)
app.add_url_rule('/new_campaign', 'new_campaign',
                 new_campaign, methods=['POST'])
app.add_url_rule('/add_comment', 'add_comment',
                 add_comment, methods=['POST'])

# Routes to manage the publications
app.add_url_rule('/submit_publication', 'submit_publication',
                 submit_publication, methods=['GET', 'POST'])
app.add_url_rule('/publications', 'publications', publications)
# Get the user id when someone like or dislike a publication
app.add_url_rule('/like/<int:publication_id>',
                 'like_publication', like_publication, methods=['POST'])
app.add_url_rule('/dislike/<int:publication_id>',
                 'dislike_publication', dislike_publication,
                 methods=['POST'])

denounce_controller = DenounceApp()

# Routes to manage the denounces interfaces
app.add_url_rule('/denounce', 'denounce', denounce_controller.denounce)
app.add_url_rule('/denounce_form', 'denounce_form',
                 denounce_controller.denounce_form)
app.add_url_rule('/submit_denuncia', 'submit_denuncia',
                 denounce_controller.submit_denuncia, methods=['POST'])

'''
    The section of the Forum is divided into three categories:
    Debates: intended for opinions on a specific topic.
    Questions: intended for creating specific questions.
    Threads: for people who want to talk openly about a topic.
'''
# Create an instance of ForumController
forum_controller = ForumController()

# Add all the routes using app.add_url_rule
app.add_url_rule('/forum', 'forum', login_required(forum_controller.forum))
app.add_url_rule('/responses', 'responses', login_required(forum_controller.responses))

# Debate-related routes
app.add_url_rule('/new_debate', 'new_debate',
                 login_required(forum_controller.new_debate), methods=['POST'])
app.add_url_rule('/edit_debate/<int:debate_id>',
                 'edit_debate', login_required(forum_controller.edit_debate), methods=['GET', 'POST'])
app.add_url_rule('/delete_debate/<int:debate_id>',
                 'delete_debate', login_required(forum_controller.delete_debate), methods=['POST'])

# Question-related routes
app.add_url_rule('/new_question', 'new_question',
                 login_required(forum_controller.new_question), methods=['POST'])
app.add_url_rule('/edit_question/<int:question_id>',
                 'edit_question', login_required(forum_controller.edit_question), methods=['GET', 'POST'])
app.add_url_rule('/delete_question/<int:question_id>',
                 'delete_question', login_required(forum_controller.delete_question), methods=['POST'])

# Thread-related routes
app.add_url_rule('/new_thread',
                 'new_thread', login_required(forum_controller.new_thread), methods=['POST'])
app.add_url_rule('/edit_thread/<int:thread_id>',
                 'edit_thread', login_required(forum_controller.edit_thread), methods=['GET', 'POST'])
app.add_url_rule('/delete_thread/<int:thread_id>',
                 'delete_thread', login_required(forum_controller.delete_thread), methods=['POST'])


'''
    The next three routes are to get all the debates, questions,
    and threads from the database and display them on the main template.
'''
app.add_url_rule('/get_all_debates', 'get_all_debates',
                 get_all_debates)
app.add_url_rule('/get_all_questions', 'get_all_questions',
                 get_all_questions)
app.add_url_rule('/get_all_threads', 'get_all_threads',
                 get_all_threads)

'''
    The next three routes are for getting the forum content,
    based on the ID to associate it with an answer when it's added.
'''
app.add_url_rule('/get_debate_by_id/<int:debate_id>',
                 'get_debate_by_id', get_debate_by_id)
app.add_url_rule('/get_question_by_id/<int:question_id>',
                 'get_question_by_id', get_question_by_id)
app.add_url_rule('/get_thread_by_id/<int:thread_id>',
                 'get_thread_by_id', get_thread_by_id)

'''
This route is the template to loading the sponsor publication.
pp stands for 'patrocinar publicacion'
'''
app.add_url_rule('/pp','pp', pp, methods=['GET', 'POST'])

'''
    Independents routes for static pages.
    Those pages bellow are for provide information and not have dynamic.
'''


# Sustainable (productos sostenibles) routes
@app.route('/sustainable_products')
def sustainable_products():
    return render_template('sustainable_products.html')

@app.route('/documentation')
def documentation():
    return render_template('05Manual_de_uso.html')

# Ruta de la interfaz de Biodiversidad en Nicaragua
@app.route('/biodiversity')
def biodiversity():
    return render_template('biodiversity.html')

@app.route('/deforestation')
def deforestation():
    return render_template('deforestation.html')

@app.route('/gei')
def gei():
    return render_template('gei.html')

@app.route('/cf')
def cf():
    return render_template('cf.html')

@app.route('/dcp')
def dcp():
    return render_template('dcp.html')

@app.route('/anm')
def anm():
    return render_template('anm.html')


@app.route('/alpp')
def alpp():
    return render_template('alpp.html')

@app.route('/droughts')
def droughts():
    return render_template('droughts.html')

@app.route('/inundations')
def inundations():
    return render_template('inundations.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/sustainability')
def sustainability():
    return render_template('sustainability.html')

@app.route('/natural_resources')
def natural_resources():
    return render_template('natural_resources.html')

@app.route('/renewable_energy')
def renewable_energy():
    return render_template('renewable_energy.html')

@app.route('/energy_efficiency')
def energy_efficiency():
    return render_template('energy_efficiency.html')

@app.route('/sustainable_transport')
def sustainable_transport():
    return render_template('sustainable_transport.html')

@app.route('/sustainable_agriculture')
def sustainable_agriculture():
    return render_template('agriculture.html')

@app.route('/ecosystem')
def ecosystem():
    return render_template('ecosystems.html')

@app.route('/sustainable_diet')
def sustainable_diet():
    return render_template('sustainable_diet.html')

@app.route('/recycle')
def recycle():
    return render_template('recycle.html')

@app.route('/environmental_policies')
def environmental_policies():
    return render_template('environment_policies.html')

@app.route('/technology')
def technology():
    return render_template('technology.html')

@app.route('/public_awareness')
def public_awareness():
    return render_template('public_awareness.html')

if __name__ == '__main__':
    app.run(debug=True)
