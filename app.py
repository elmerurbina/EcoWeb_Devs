from flask import Flask, render_template
from autenticacion import register, login, campanias, foro

app = Flask(__name__)

@app.route('/cs')
def index():
    return render_template('index.html')

@app.route('/ep')
def ep():
    return render_template('empresasSostenibles.html')



app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/foro', 'foro', foro)
app.add_url_rule('/campanias', 'campanias', campanias)

if __name__ == '__main__':
    app.run(debug=True)
