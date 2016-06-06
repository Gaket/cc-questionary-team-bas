from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import json
import os

from random import randrange


def write_answer(qs):
    """
    This method writes the incoming data structure into json with a random hash number
    :param qs: structure od answers for raw files
    """
    hash_ = randrange(2197000)
    session['answer'] = str(hash_)
    filename = 'questionary_' + str(hash_) + '.json'
    with open(os.path.join('app',
                           'data',
                           'raw',
                           filename), 'w') as fp:
        json.dump(qs, fp, sort_keys=True, indent=4)


@app.route('/', methods=['GET', 'POST'])
def hello():
    survey = Survey("app/data/questions.json", "en")
    if request.method == 'GET':
        return render_template('index.html', survey=survey, lang="en")
    elif request.method == 'POST':
        qs = getData(survey)
        write_answer(qs)
        return render_template('thankyou.html', results=qs)


@app.route('/ru', methods=['GET', 'POST'])
def helloRu():
    survey = Survey("app/data/questions.json", "ru")
    if request.method == 'GET':
        return render_template('index.html', survey=survey, lang="ru")
    elif request.method == 'POST':
        qs = getData(survey)
        write_answer(qs)
        return render_template('thankyou.html', results=qs)

def getData(survey):
    qs = dict()
    answers = list()
    for key, item in survey.questions.items():
        answer = dict()
        answer[key] = key
        if 'answer' not in answer:
            answer['answer'] = list()
        if item.type == 'mult':
            for var in item.variants:
                answer['answer'].append(request.form.get(var))
        else:
            answer['answer'].append(request.form.get(key))
        answers.append(answer)
    qs['answers'] = answers



@app.route('/results')
def chart():
    labels = ['First', 'second', 'third variant', "and here some other"]
    values = [1, 9, 3, 2]
    return render_template('results.html', values=values, labels=labels)


@app.route('/login', methods=['GET', 'POST'])
def check_login():
    if request.method.lower() == 'get':
        msg = "Pleas enter username and password to access survey statistics"
        return render_template('login.html', message=msg)
    elif request.method.lower() == 'post':
        if request.form['user'] == 'admin' and \
                request.form['password'] == 'secret':
            session['admin'] = True
            return redirect(url_for('get_statistics'))
        else:
            return render_template('login.html', message="Wrong user or password")


@app.route('/statistics')
def get_statistics():
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    else:
        data = json.load(open(os.path.join('app',
                                      'data',
                                      'aggregated_data.json')))
        chart_labels = list()
        chart_values = list()
        for ans in data:
            if ans['key'] == 'about DB':
                for elem, val in ans['answer'].items():
                    chart_labels.append(elem)
                    chart_values.append(float(val))
        data.append(chart_labels)
        data.append(chart_values)
        return render_template('statistics.html', data=data)


@app.route('/results/<int:uid>')
def get_results(uid):
    data = dict()
    msg = ''
    result_path = 'questionary_' + str(uid) + '.json'
    if not os.path.exists(result_path):
        msg = "Results were not found, please check results address."
    else:
        msg = "Survey {0}".format(str(uid))
        data = json.load(open(os.path.join('app',
                                           'data',
                                           'raw',
                                           result_path)))
    return render_template('results.html', data=data, msg=msg)


@app.route('/results')
@app.route('/results/')
def result():
    if 'answer' in session:
        return redirect('/results/' + str(session['answer']))
    else:
        msg = "To see the results, please complete the survey"
        return render_template('results.html', data=dict(), msg=msg)
