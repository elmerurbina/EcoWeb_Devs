# Archivo para manejar la lógica del Foro

# Importación de librerías y módulos
from flask import Flask, render_template, request, url_for, redirect, flash
from models.forum_model import (
    ForoDebate, ForoHilo, ForoPregunta, get_all_debates, get_all_questions, get_all_threads,
    save_response, get_respuestas, create_connection,
    get_debate_by_id, update_debate, delete_debate,
    get_question_by_id, update_question, delete_question,
    get_thread_by_id, update_thread, delete_thread
)
from settings import Config
from models.authentication_model import User
from flask_login import login_required, current_user, LoginManager

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# Definir la función de carga de usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class ForumController:
    @app.route('/forum')
    def forum(self):
        form_type = request.args.get('form_type', '')

        # Obtener los debates, preguntas y hilos de conversación desde la base de datos
        debates = get_all_debates()
        questions = get_all_questions()
        threads = get_all_threads()

        return render_template('forum.html', form_type=form_type, debates=debates, questions=questions, threads=threads)

    @app.route('/responses')
    def responses(self):
        item_id = request.args.get('item_id')
        item_type = request.args.get('item_type')

        if item_id is None or item_type is None:
            return "Item ID and Item Type are required", 400

        respuestas = get_respuestas(item_id, item_type)
        return render_template('respuestas.html', respuestas=respuestas)

    @app.route('/new_debate', methods=['POST'])
    @login_required
    def new_debate(self):
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        punto_de_vista = request.form['punto-de-vista']
        otras_observaciones = request.form.get('otras-observaciones', '')
        autor_id = current_user.id

        try:
            ForoDebate.save(titulo, descripcion, punto_de_vista, otras_observaciones, autor_id)
            flash('El debate se agregó con éxito', 'success')
        except Exception as e:
            flash(f'Error al agregar el debate: {str(e)}', 'error')

        return redirect(url_for('forum'))

    @app.route('/edit_debate/<int:debate_id>', methods=['GET', 'POST'])
    @login_required
    def edit_debate(debate_id):
        debate = get_debate_by_id(debate_id)
        if debate is None:
            flash('Debate no encontrado', 'error')
            return redirect(url_for('foro'))

        if debate['autor_id'] != current_user.id:
            flash('No tienes permiso para editar este debate', 'error')
            return redirect(url_for('foro'))

        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            punto_de_vista = request.form['punto-de-vista']
            otras_observaciones = request.form.get('otras-observaciones', '')

            try:
                update_debate(debate_id, titulo, descripcion, punto_de_vista, otras_observaciones)
                flash('Debate actualizado exitosamente', 'success')
                return redirect(url_for('foro'))
            except Exception as e:
                flash(f'Error al actualizar el debate: {str(e)}', 'error')
        return render_template('edit_debate.html', debate=debate)

    @app.route('/delete_debate/<int:debate_id>', methods=['POST'])
    @login_required
    def delete_debate(debate_id):
        debate = get_debate_by_id(debate_id)
        if debate is None:
            flash('Debate no encontrado', 'error')
            return redirect(url_for('foro'))

        if debate['autor_id'] != current_user.id:
            flash('No tienes permiso para eliminar este debate', 'error')
            return redirect(url_for('foro'))

        try:
            delete_debate(debate_id)
            flash('Debate eliminado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al eliminar el debate: {str(e)}', 'error')

        return redirect(url_for('foro'))

    # Rutas similares para preguntas
    @app.route('/new_question', methods=['POST'])
    @login_required
    def new_question(self):
        titulo = request.form['titulo']
        pregunta = request.form.get('question-input', '')
        autor_id = current_user.id

        try:
            ForoPregunta.save(titulo, pregunta, autor_id)
            flash('Se publicó tu pregunta', 'success')
        except Exception as e:
            flash(f'Error al publicar la pregunta: {str(e)}', 'error')

        return redirect(url_for('forum'))

    @app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
    @login_required
    def edit_question(question_id):
        question = get_question_by_id(question_id)
        if question is None:
            flash('Pregunta no encontrada', 'error')
            return redirect(url_for('foro'))

        if question['autor_id'] != current_user.id:
            flash('No tienes permiso para editar esta pregunta', 'error')
            return redirect(url_for('foro'))

        if request.method == 'POST':
            titulo = request.form['titulo']
            pregunta = request.form.get('question-input', '')

            try:
                update_question(question_id, titulo, pregunta)
                flash('Pregunta actualizada exitosamente', 'success')
                return redirect(url_for('foro'))
            except Exception as e:
                flash(f'Error al actualizar la pregunta: {str(e)}', 'error')
        return render_template('edit_question.html', question=question)

    @app.route('/delete_question/<int:question_id>', methods=['POST'])
    @login_required
    def delete_question(question_id):
        question = get_question_by_id(question_id)
        if question is None:
            flash('Pregunta no encontrada', 'error')
            return redirect(url_for('foro'))

        if question['autor_id'] != current_user.id:
            flash('No tienes permiso para eliminar esta pregunta', 'error')
            return redirect(url_for('foro'))

        try:
            delete_question(question_id)
            flash('Pregunta eliminada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al eliminar la pregunta: {str(e)}', 'error')

        return redirect(url_for('foro'))

    # Rutas similares para hilos de conversación
    @app.route('/new_thread', methods=['POST'])
    @login_required
    def new_thread(self):
        titulo = request.form['conversation-title']
        tema = request.form.get('conversation-topic', '')
        autor_id = current_user.id

        try:
            ForoHilo.save(titulo, tema, autor_id)
            flash('Conversación agregada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al agregar la conversación: {str(e)}', 'error')

        return redirect(url_for('foro'))

    @app.route('/edit_thread/<int:thread_id>', methods=['GET', 'POST'])
    @login_required
    def edit_thread(thread_id):
        thread = get_thread_by_id(thread_id)
        if thread is None:
            flash('Hilo no encontrado', 'error')
            return redirect(url_for('foro'))

        if thread['autor_id'] != current_user.id:
            flash('No tienes permiso para editar este hilo', 'error')
            return redirect(url_for('foro'))

        if request.method == 'POST':
            titulo = request.form['titulo']
            tema = request.form.get('tema', '')

            try:
                update_thread(thread_id, titulo, tema)
                flash('Hilo actualizado exitosamente', 'success')
                return redirect(url_for('foro'))
            except Exception as e:
                flash(f'Error al actualizar el hilo: {str(e)}', 'error')
        return render_template('edit_thread.html', thread=thread)

    @app.route('/delete_thread/<int:thread_id>', methods=['POST'])
    @login_required
    def delete_thread(thread_id):
        thread = get_thread_by_id(thread_id)
        if thread is None:
            flash('Hilo no encontrado', 'error')
            return redirect(url_for('foro'))

        if thread['autor_id'] != current_user.id:
            flash('No tienes permiso para eliminar este hilo', 'error')
            return redirect(url_for('foro'))

        try:
            delete_thread(thread_id)
            flash('Hilo eliminado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al eliminar el hilo: {str(e)}', 'error')

        return redirect(url_for('foro'))

    # Ruta para mostrar el perfil de usuario
    @app.route('/profile')
    @login_required
    def profile(self):
        return render_template('profile.html', user=current_user)

    # Ruta para crear una nueva respuesta
    @app.route('/new_response', methods=['POST'])
    @login_required
    def new_response(self):
        respuesta = request.form['respuesta']
        item_id = request.form['item_id']
        item_type = request.form['item_type']
        autor_id = current_user.id

        success = save_response(respuesta, item_id, item_type, autor_id)
        if success:
            return redirect(url_for('respuestas', item_id=item_id, item_type=item_type))
        else:
            flash('Error al guardar la respuesta', 'error')
            return redirect(url_for('respuestas', item_id=item_id, item_type=item_type))

# Inicializar el controlador del foro
ForumController()
