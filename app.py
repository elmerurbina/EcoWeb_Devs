from flask import Flask, render_template
from autenticacion import register, login
from publicaciones import publicaciones
from campanias import campanias, new_campaign
from denuncia import denuncia, denunciaForm, submit_denuncia
from foro import foro, new_debate, new_thread, new_question
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/verdeNica')
def verdeNica():
    return render_template('index.html')

@app.route('/ep')
def ep():
    return render_template('empresasSostenibles.html')



app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])

#app.add_url_rule('/foro', 'foro', foro)
app.add_url_rule('/campanias', 'campanias', campanias)
app.add_url_rule('/new_campaign', 'new_campaign', new_campaign, methods=['POST'])


app.add_url_rule('/publicaciones', 'publicaciones', publicaciones)

app.add_url_rule('/denuncia', 'denuncia', denuncia)
app.add_url_rule('/denunciaForm', 'denunciaForm', denunciaForm)
app.add_url_rule('/submit_denuncia', 'submit_denuncia', submit_denuncia, methods=['POST'])

app.add_url_rule('/foro', 'foro', foro)
app.add_url_rule('/new_debate', 'new_debate', new_debate, methods=['POST'])
app.add_url_rule('/new_question', 'new_question', new_question, methods=['POST'])
app.add_url_rule('/new_thread', 'new_thread', new_thread, methods=['POST'])


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

if __name__ == '__main__':
    app.run(debug=True)
