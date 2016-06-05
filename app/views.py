from app import app
from app.main.survey import Survey
from flask import render_template

@app.route('/')
def hello():
    survey = Survey("app/data/questions.json")
    return render_template('index.html', survey=survey)

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