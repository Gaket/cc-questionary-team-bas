from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request

@app.route('/')
def hello():
    survey = Survey("app/data/questions.json")
    return render_template('index.html', survey=survey)

# @app.route('/')
# def world():
#     user = {'nickname': 'You' }
#     return render_template("base.html",
#                            title = 'World',
#                            user = user)

@app.route('/temp')
def temp():
    return "Temp"

@app.route('/results')
def result():
    return request.form.get('name_MySQL')

# @app.route('/hash/<int:survey_hash>', methods=['POST'])
# def send_result(survey_hash):
#     pass