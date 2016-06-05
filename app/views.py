from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request

@app.route('/', methods=['GET', 'POST'])
def hello():
    survey = Survey("app/data/questions.json")
    if request.method == 'GET':
        return render_template('index.html', survey=survey)
    elif request.method == 'POST':
        res = list()
        for key, item in survey.questions.items():
            if item.type == 'mult':
                for var in item.variants:
                    res.append(request.form.get(var))
            res.append(request.form.get(key))
        return render_template('results.html', results=res)

# @app.route()
# def process_question():
#     pass

# @app.route('/')
# def world():
#     user = {'nickname': 'You' }
#     return render_template("base.html",
#                            title = 'World',
#                            user = user)

@app.route('/results')
def chart():
    labels = ['First', 'second', 'third variant', "and here some other"]
    values = [1, 9, 3, 2]
    return render_template('results.html', values=values, labels=labels)

# @app.route('/')
# def result():
#     return request.form.get('about DB')

# @app.route('/hash/<int:survey_hash>', methods=['POST'])
# def send_result(survey_hash):
#     pass