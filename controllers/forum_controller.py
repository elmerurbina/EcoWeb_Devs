# File to handle the logic of the Forum

# Importing libraries and modules
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
from flask_login import login_required, current_user, LoginManager  # For authentication

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# Define the user loading function
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class ForumController:
    """Controller to handle forum logic."""

    @app.route('/forum')
    def forum(self):
        """Renders the main forum page."""
        form_type = request.args.get('form_type', '')

        debates = get_all_debates()
        questions = get_all_questions()
        threads = get_all_threads()

        return render_template('forum.html', form_type=form_type, debates=debates, questions=questions, threads=threads)

    @app.route('/responses')
    def responses(self):
        """Displays the responses for a debate, question, or thread."""
        item_id = request.args.get('item_id')
        item_type = request.args.get('item_type')

        if item_id is None or item_type is None:
            return "Item ID and Item Type are required", 400

        responses = get_respuestas(item_id, item_type)
        return render_template('responses.html', responses=responses)

    # Debate-related methods
    @app.route('/new_debate', methods=['POST'])
    @login_required
    def new_debate(self):
        """Adds a new debate."""
        title = request.form['title']
        description = request.form['description']
        point_of_view = request.form['point-of-view']
        additional_observations = request.form.get('additional-observations', '')
        author_id = current_user.id

        try:
            ForoDebate.save(title, description, point_of_view, additional_observations, author_id)
            flash('The debate was successfully added', 'success')
        except Exception as e:
            flash(f'Error adding the debate: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    @app.route('/edit_debate/<int:debate_id>', methods=['GET', 'POST'])
    @login_required
    def edit_debate(debate_id):
        """Edits an existing debate."""
        debate = get_debate_by_id(debate_id)
        if debate is None:
            flash('Debate not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if debate['author_id'] != current_user.id:
            flash('You do not have permission to edit this debate', 'error')
            return redirect(url_for('ForumController.forum'))

        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            point_of_view = request.form['point-of-view']
            additional_observations = request.form.get('additional-observations', '')

            try:
                update_debate(debate_id, title, description, point_of_view, additional_observations)
                flash('Debate updated successfully', 'success')
                return redirect(url_for('ForumController.forum'))
            except Exception as e:
                flash(f'Error updating the debate: {str(e)}', 'error')

        return render_template('edit_debate.html', debate=debate)

    @app.route('/delete_debate/<int:debate_id>', methods=['POST'])
    @login_required
    def delete_debate(debate_id):
        """Deletes a debate."""
        debate = get_debate_by_id(debate_id)
        if debate is None:
            flash('Debate not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if debate['author_id'] != current_user.id:
            flash('You do not have permission to delete this debate', 'error')
            return redirect(url_for('ForumController.forum'))

        try:
            delete_debate(debate_id)
            flash('Debate deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting the debate: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    # Question-related methods
    @app.route('/new_question', methods=['POST'])
    @login_required
    def new_question(self):
        """Adds a new question."""
        title = request.form['title']
        question = request.form.get('question-input', '')
        author_id = current_user.id

        try:
            ForoPregunta.save(title, question, author_id)
            flash('Your question was posted', 'success')
        except Exception as e:
            flash(f'Error posting the question: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    @app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
    @login_required
    def edit_question(question_id):
        """Edits an existing question."""
        question = get_question_by_id(question_id)
        if question is None:
            flash('Question not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if question['author_id'] != current_user.id:
            flash('You do not have permission to edit this question', 'error')
            return redirect(url_for('ForumController.forum'))

        if request.method == 'POST':
            title = request.form['title']
            question_text = request.form.get('question-input', '')

            try:
                update_question(question_id, title, question_text)
                flash('Question updated successfully', 'success')
                return redirect(url_for('ForumController.forum'))
            except Exception as e:
                flash(f'Error updating the question: {str(e)}', 'error')

        return render_template('edit_question.html', question=question)

    @app.route('/delete_question/<int:question_id>', methods=['POST'])
    @login_required
    def delete_question(question_id):
        """Deletes a question."""
        question = get_question_by_id(question_id)
        if question is None:
            flash('Question not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if question['author_id'] != current_user.id:
            flash('You do not have permission to delete this question', 'error')
            return redirect(url_for('ForumController.forum'))

        try:
            delete_question(question_id)
            flash('Question deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting the question: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    # Thread-related methods
    @app.route('/new_thread', methods=['POST'])
    @login_required
    def new_thread(self):
        """Adds a new thread."""
        title = request.form['title']
        thread_content = request.form.get('thread-input', '')
        author_id = current_user.id

        try:
            ForoHilo.save(title, thread_content, author_id)
            flash('Thread successfully created', 'success')
        except Exception as e:
            flash(f'Error creating the thread: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    @app.route('/edit_thread/<int:thread_id>', methods=['GET', 'POST'])
    @login_required
    def edit_thread(thread_id):
        """Edits an existing thread."""
        thread = get_thread_by_id(thread_id)
        if thread is None:
            flash('Thread not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if thread['author_id'] != current_user.id:
            flash('You do not have permission to edit this thread', 'error')
            return redirect(url_for('ForumController.forum'))

        if request.method == 'POST':
            title = request.form['title']
            thread_content = request.form.get('thread-input', '')

            try:
                update_thread(thread_id, title, thread_content)
                flash('Thread updated successfully', 'success')
                return redirect(url_for('ForumController.forum'))
            except Exception as e:
                flash(f'Error updating the thread: {str(e)}', 'error')

        return render_template('edit_thread.html', thread=thread)

    @app.route('/delete_thread/<int:thread_id>', methods=['POST'])
    @login_required
    def delete_thread(thread_id):
        """Deletes a thread."""
        thread = get_thread_by_id(thread_id)
        if thread is None:
            flash('Thread not found', 'error')
            return redirect(url_for('ForumController.forum'))

        if thread['author_id'] != current_user.id:
            flash('You do not have permission to delete this thread', 'error')
            return redirect(url_for('ForumController.forum'))

        try:
            delete_thread(thread_id)
            flash('Thread deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting the thread: {str(e)}', 'error')

        return redirect(url_for('ForumController.forum'))

    @app.route('/profile')
    @login_required
    def profile(self):
        """Displays user profile."""
        return render_template('profile.html', user=current_user)

