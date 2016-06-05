from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        survey = Survey("app/data/questions.json")
        return render_template('index.html', survey=survey)
    elif request.method == 'POST':
        pass


@app.route('/survey/')
def process_question():
    pass
# @app.route('/')
# def world():
#     user = {'nickname': 'You' }
#     return render_template("layout.html",
#                            title = 'World',
#                            user = user)


@app.route('/temp')
def temp():
    return "Temp"

# @app.route('/hash/<int:survey_hash>', methods=['POST'])
# def send_result(survey_hash):
#     pass
