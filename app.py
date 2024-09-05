from flask import Flask, render_template
from autenticacion import register, login, nuevasCredenciales, recuperarCuenta
from publicaciones import submit_publication, publicaciones
from campanias import campanias, new_campaign, add_comment
from denuncia import denuncia, denunciaForm, submit_denuncia
from foro import foro, new_debate, new_thread, new_question, new_response, respuestas
from config import Config
from submit_publication import submit_publication
from ia import recognize
from PatrocinarPublicacion import pp

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/verdeNica')
def verdeNica():
    return render_template('index.html')

@app.route('/ep')
def ep():
    return render_template('empresasSostenibles.html')

@app.route('/biodiversidad')
def biodiversidad():
    return render_template('biodiversidad.html')


app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/recuperarCuenta', 'recuperarCuenta', recuperarCuenta)
app.add_url_rule('/nuevasCredenciales', 'nuevasCredenciales', nuevasCredenciales)

#app.add_url_rule('/foro', 'foro', foro)
app.add_url_rule('/campanias', 'campanias', campanias)
app.add_url_rule('/new_campaign', 'new_campaign', new_campaign, methods=['POST'])
app.add_url_rule('/add_comment', 'add_comment', add_comment, methods=['POST'])


app.add_url_rule('/submit_publication', 'submit_publication', submit_publication, methods=['GET', 'POST'])
app.add_url_rule('/publicaciones', 'publicaciones', publicaciones)



app.add_url_rule('/denuncia', 'denuncia', denuncia)
app.add_url_rule('/denunciaForm', 'denunciaForm', denunciaForm)
app.add_url_rule('/submit_denuncia', 'submit_denuncia', submit_denuncia, methods=['POST'])

app.add_url_rule('/foro', 'foro', foro)
app.add_url_rule('/new_debate', 'new_debate', new_debate, methods=['POST'])
app.add_url_rule('/new_question', 'new_question', new_question, methods=['POST'])
app.add_url_rule('/new_thread', 'new_thread', new_thread, methods=['POST'])
app.add_url_rule('/new_response', 'new_response', new_response, methods=['POST'])
app.add_url_rule('/respuestas', 'respuestas', respuestas)

app.add_url_rule('/pp','pp', pp, methods=['GET', 'POST'])


@app.route('/ia', methods=['GET'])
def ia():
    return render_template('ia.html')

# Register the 'recognize' route from the ia module
app.add_url_rule('/recognize', 'recognize', recognize, methods=['POST'])


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
