from flask import Blueprint

questions = Blueprint('questions', __name__, template_folder='templates/questions')


@questions.route('', defaults={'page': 1, 'sort': 'newest'})
@questions.route('?page=<page>', defaults={'sort': 'newest'})
@questions.route('?sort=<sort>', defaults={'page': 1})
@questions.route('?page=<page>&sort=<sort>')
def list_questions(page, sort):
    return 'Questions'
