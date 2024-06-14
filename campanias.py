from flask import Flask, render_template

app = Flask(__name__)

@app.route('/campanias')
def campanias():
    return render_template('campanias.html')

if __name__ == '__main__':
    app.run(debug=True)