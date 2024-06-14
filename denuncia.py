from flask import Flask, render_template

app = Flask(__name__)

@app.route('/denuncia')
def denuncia():
    return render_template('denuncia.html')

if __name__ == '__main__':
    app.run(debug=True)