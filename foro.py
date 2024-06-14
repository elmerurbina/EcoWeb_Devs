from flask import Flask, render_template

app = Flask(__name__)

@app.route('/foro')
def foro():
    return render_template('foro.html')

if __name__ == '__main__':
    app.run(debug=True)