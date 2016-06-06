from app import app
from app.main.const import QUESTIONS_ADDR
from app.main.survey import Survey, getQuestions
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import json
import os

from random import randrange


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/main/<lang>', methods=['GET', 'POST'])
def hello(lang="en"):
    survey = Survey("app/data/questions.json", lang)
    if request.method == 'GET':
        return render_template('index.html', survey=survey, lang=lang)
    elif request.method == 'POST':
        qs = getData(survey)
        write_answer(qs)
        write_aggregated(qs)
        return render_template('thankyou.html', results=qs, lang=lang)


def getData(survey):
    qs = []
    for key, item in survey.questions.items():
        answer = []
        if item.type == 'mult':
            for var in item.variants:
                if (request.form.get(var) is not None):
                    answer.append(request.form.get(var))
        else:
            answer.append(request.form.get(key))
        qs.append({"question_id": key, "answer": answer})
    return qs


def write_answer(qs):
    """
    This method writes the incoming data structure into json with a random hash number
    :param qs: structure od answers for raw files
    """
    hash = randrange(2197000)
    with open('app//data//raw//result_' + str(hash) + '.json', 'w') as fp:
        json.dump(qs, fp, sort_keys=True, indent=4)


def write_aggregated(qs):
    # with open('app//data//raw//result_' + str(hash) + '.json', 'w') as fp:
    #     for element in qs:
    #         for key, value in element:

    pass




@app.route('/results')
def chart():
    labels = ['First', 'second', 'third variant', "and here some other"]
    values = [1, 9, 3, 2]
    return render_template('results.html', values=values, labels=labels)


@app.route('/login/<lang>', methods=['GET', 'POST'])
def check_login(lang="en"):
    if request.method.lower() == 'get':
        msg = "Pleas enter username and password to access survey statistics"
        return render_template('login.html', message=msg, lang=lang)
    elif request.method.lower() == 'post':
        if request.form['user'] == 'admin' and \
                        request.form['password'] == 'secret':
            session['admin'] = True
            return redirect(url_for('get_statistics'))
        else:
            return render_template('login.html', message="Wrong user or password", lang=lang)


@app.route('/statistics/<lang>')
def get_statistics(lang="en"):
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    else:
        questions = getQuestions(QUESTIONS_ADDR, lang)
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
        return render_template('statistics.html', data=data, lang=lang)
