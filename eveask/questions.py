from flask import Blueprint, render_template

questions = Blueprint('questions', __name__, template_folder='templates/questions')


@questions.route('', defaults={'page': 1, 'sort': 'newest'})
@questions.route('?page=<page>', defaults={'sort': 'newest'})
@questions.route('?sort=<sort>', defaults={'page': 1})
@questions.route('?page=<page>&sort=<sort>')
def list_questions(page, sort):
    return render_template('questions.html')


@questions.route('/new', methods=['GET', 'POST'])
def new_question():
    return render_template('new_question.html')
