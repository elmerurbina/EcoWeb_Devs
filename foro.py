# Archivo para manejar la logica del Foro


# Importacion de librerias y modulos
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from db import ForoDebate, ForoHilo, ForoPregunta, get_all_debates, get_all_questions, get_all_threads, save_response, \
    get_respuestas, create_connection
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

# Ruta para la interfaz principal
@app.route('/foro')
def foro():
    form_type = request.args.get('form_type', '')

    # Obtener los debates, preguntas y hilos de conversacion desde la base de datos
    debates = get_all_debates()
    questions = get_all_questions()
    threads = get_all_threads()

    # Obtener las respuestas
    respuestas = get_respuestas()

    # Crear un diccionario para mappear el id y el item type de las respuestas
    respuestas_dict = {}
    for respuesta in respuestas:
        key = ()
        if key not in respuestas_dict:
            respuestas_dict[key] = []
        respuestas_dict[key].append(respuesta)

    return render_template('foro.html', form_type=form_type, debates=debates, questions=questions, threads=threads,
                           respuestas_dict=respuestas_dict)


# Ruta para agregar un nuevo debate
@app.route('/new_debate', methods=['POST'])
def new_debate():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    punto_de_vista = request.form['punto-de-vista']
    otras_observaciones = request.form.get('otras-observaciones', '')

    try:
        # Validar que todos los campos se hayan llenado correctamente
        ForoDebate.save(titulo, descripcion, punto_de_vista, otras_observaciones)
        flash('El debate se agregó con éxito', 'success')
    except Exception as e:
        flash(f'Error al agregar el debate: {str(e)}', 'error')

    return redirect(url_for('foro'))

# Ruta para agregar una nueva pregunta
@app.route('/new_question', methods=['POST'])
def new_question():
    titulo = request.form['titulo']
    pregunta = request.form.get('question-input', '')

    try:
        # Validar los campos esten correctos
        ForoPregunta.save(titulo, pregunta)
        flash('Se publicó tu pregunta', 'success')
    except Exception as e:
        flash(f'Error al publicar la pregunta: {str(e)}', 'error')

    return redirect(url_for('foro'))


# Nuevo hilo de conversacion
@app.route('/new_thread', methods=['POST'])
def new_thread():
    titulo = request.form['conversation-title']
    tema = request.form.get('conversation-topic', '')

    try:
        # Validar que los campos requeridos no esten vacios
        ForoHilo.save(titulo, tema)
        flash('Conversación agregada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar la conversación: {str(e)}', 'error')

    return redirect(url_for('foro'))

# Nueva respuesta
@app.route('/new_response', methods=['POST'])
def new_response():
    respuesta = request.form['respuesta']

    success = save_response(respuesta)
    if success:
        return redirect('/respuestas') # Redirigir a la ruta de las respuesta
    else:
        return "Error saving response", 500

# Ruta para la interfaz de las respuestas
@app.route('/respuestas')
def respuestas():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all responses
        cursor.execute('SELECT * FROM respuestas')
        respuestas = cursor.fetchall()

        return render_template('respuestas.html', respuestas=respuestas)
    except Exception as e:
        print(f"Error: {e}")
        return "Error retrieving responses", 500
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)