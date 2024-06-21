from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/foro')
def foro():
    form_type = request.args.get('form_type', '')
    return render_template('foro.html', form_type=form_type)

if __name__ == '__main__':
    app.run(debug=True)