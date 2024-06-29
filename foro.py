from flask import Flask, render_template, request, url_for, redirect, flash
from db import ForoDebate, ForoHilo, ForoPregunta

app = Flask(__name__)


@app.route('/foro')
def foro():
    form_type = request.args.get('form_type', '')
    return render_template('foro.html', form_type=form_type)


@app.route('/new_debate', methods=['POST'])
def new_debate():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    punto_de_vista = request.form['punto-de-vista']
    otras_observaciones = request.form.get('otras-observaciones', '')


    try:
        ForoDebate.save(titulo, descripcion, punto_de_vista, otras_observaciones)
        flash('El debate se agregó con éxito', 'success')
    except Exception as e:
        flash(f'Error al agregar el debate: {str(e)}', 'error')

    return redirect(url_for('foro'))

@app.route('/new_question', methods=['POST'])
def new_question():
    titulo = request.form['titulo']
    pregunta = request.form.get('question-input', '')

    # Attempt to save the question
    try:
        ForoPregunta.save(titulo, pregunta)
        flash('Se publicó tu pregunta', 'success')
    except Exception as e:
        flash(f'Error al publicar la pregunta: {str(e)}', 'error')

    return redirect(url_for('foro'))

@app.route('/new_thread', methods=['POST'])
def new_thread():
    titulo = request.form['conversation-title']
    tema = request.form.get('conversation-topic', '')


    try:
        ForoHilo.save(titulo, tema)
        flash('Conversación agregada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar la conversación: {str(e)}', 'error')

    return redirect(url_for('foro'))


if __name__ == '__main__':
    app.run(debug=True)