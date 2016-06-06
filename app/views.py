import codecs

from app import app
from app.main.const import QUESTIONS_ADDR
from app.main.const import AGGREGATED_ADDR
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
def hello():
    if 'lang' not in session:
        session['lang'] = 'en'
    survey = Survey("app/data/questions.json", lang=session['lang'])
    if request.method == 'GET':
        return render_template('index.html', survey=survey, lang=session['lang'])
    elif request.method == 'POST':
        qs = getData(survey)
        write_answer(qs)
        write_aggregated(qs)
        return render_template('thankyou.html', results=qs, lang=session['lang'])


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
    aggregated = json.load(codecs.open(AGGREGATED_ADDR, 'r', 'utf-8-sig'))
    questions = json.load(codecs.open(QUESTIONS_ADDR, 'r', 'utf-8-sig'))
    for element in qs:
        id_ = element["question_id"]
        # Ответ к id
        type_ = questions[id_]["type"]
        agg_answer = aggregated[id_]['answer']
        print(element)
        print(type(id_), id_)
        print(type_)
        answer = element['answer']
        # Проверить три типа вопросов, добавить ответы для каждого
        if type_ == "num":
            agg_answer[int(answer[0])-1] += 1
        elif type_ == 'open':
            agg_answer.append(answer[0])
        elif type_ == 'mult':
            for ans in answer:
                index = questions[id_][session['lang']]['variants'].index(ans)
                agg_answer[index] += 1
        aggregated[id_]['answer'] = agg_answer
    # записать агрегированные данные
    with open(AGGREGATED_ADDR, 'w') as fh:
        json.dump(aggregated, fh, sort_keys=True, indent=4)


@app.route('/login', methods=['GET', 'POST'])
def check_login():
    if request.method.lower() == 'get':
        msg = "Pleas enter username and password to access survey statistics"
        return render_template('login.html', message=msg, lang=session['lang'])
    elif request.method.lower() == 'post':
        if request.form['user'] == 'admin' and \
                        request.form['password'] == 'secret':
            session['admin'] = True
            return redirect(url_for('get_statistics'))
        else:
            return render_template('login.html', message="Wrong user or password", lang=session['lang'])


@app.route('/statistics/<lang>')
def get_statistics(lang="en"):
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    else:
        questions = getQuestions(QUESTIONS_ADDR, session['lang'])
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
        return render_template('statistics.html', data=data, lang=session['lang'])


@app.route('/lang', methods=["POST"])
def set_lang():
    session['lang'] = request.form.get('lang')
    return redirect('/')
