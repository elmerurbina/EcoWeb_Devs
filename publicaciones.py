from flask import Flask, render_template

app = Flask(__name__)

@app.route('/publicaciones')
def publicaciones():
    return render_template('publicaciones.html')


if __name__ == '__main__':
    app.run(debug=True)