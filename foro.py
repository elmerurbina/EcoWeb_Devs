from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from db import ForoDebate, ForoHilo, ForoPregunta, get_all_debates, get_all_questions, get_all_threads, save_respuesta, \
    get_respuestas

app = Flask(__name__)


@app.route('/foro')
def foro():
    form_type = request.args.get('form_type', '')

    # Retrieve data from database
    debates = get_all_debates()
    questions = get_all_questions()
    threads = get_all_threads()

    # Retrieve responses
    respuestas = get_respuestas()  # Fetch all responses

    # Create a dictionary to map item_id and item_type to their responses
    respuestas_dict = {}
    for respuesta in respuestas:
        key = (respuesta.item_id, respuesta.item_type)
        if key not in respuestas_dict:
            respuestas_dict[key] = []
        respuestas_dict[key].append(respuesta)

    return render_template('foro.html', form_type=form_type, debates=debates, questions=questions, threads=threads,
                           respuestas_dict=respuestas_dict)



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


@app.route('/new_response', methods=['POST'])
def new_response():
    respuesta = request.form['respuesta']
    item_id = request.form.get('item_id')
    item_type = request.form.get('item_type')

    try:
        save_respuesta(respuesta)  # Save the response to the database
        flash('Respuesta agregada con éxito', 'success')
    except Exception as e:
        flash(f'Error al agregar la respuesta: {str(e)}', 'error')

    return redirect(url_for('foro'))


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer_content = data.get('answer')
    item_id = data.get('item_id')
    item_type = data.get('item_type')

    if answer_content and item_id and item_type:
        save_respuesta(answer_content, item_id, item_type)
        return jsonify({'status': 'success'})

    return jsonify({'status': 'error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
