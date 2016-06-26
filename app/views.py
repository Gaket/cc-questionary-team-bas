import codecs

from app import app
from config import QUESTIONS_ADDR, QUESTIONS_TO_SHOW, QUESTIONS_TO_STATISTICS
from app.main.data_processor import getRawData, getData, write_answer, write_aggregated
from app.main.survey import Survey, getQuestionsFromJSON
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import json
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello():
    if 'lang' not in session:
        session['lang'] = 'en'
    survey = Survey(lang=session['lang'], question_numbers=QUESTIONS_TO_SHOW)
    if request.method == 'GET':
        return render_template('index.html', survey=survey, lang=session['lang'])
    elif request.method == 'POST':
        answers = getData(survey)
        write_answer(answers)
        write_aggregated(answers)
        return render_template('thankyou.html', results=answers, lang=session['lang'])


@app.route('/login', methods=['GET', 'POST'])
def check_login():
    if 'lang' not in session:
        session['lang'] = 'en'
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


@app.route('/statistics', methods=['GET', 'POST'])
def get_statistics():
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    if 'lang' not in session:
        session['lang'] = 'en'
    else:
        questions = getQuestionsFromJSON(QUESTIONS_ADDR, session['lang'], QUESTIONS_TO_STATISTICS)
        data = json.load(open(os.path.join('app',
                                           'data',
                                           'aggregated_data.json')))
        res = dict()
        chart_labels = list()
        chart_values = list()
        for key, item in data.items():
            if questions[key].type == 'mult':
                res[key] = dict()
                chart_labels = []
                chart_values = []
                for name in questions[key].variants:
                    chart_labels.append(name)
                res[key]['labels'] = chart_labels
                for val in item['answer']:
                    chart_values.append(float(val))
                res[key]['vals'] = chart_values
            elif questions[key].type == 'num':
                res[key] = dict()
                chart_labels = []
                chart_values = []
                sum = 0
                [chart_labels.append(x) for x in range(1, 11)]
                res[key]['labels'] = chart_labels
                cnt = 0
                for val in item['answer']:
                    chart_values.append(float(val))
                    sum += float(val) * cnt
                    cnt += 1
                res[key]['vals'] = chart_values
                if len(chart_values):
                    res[key]['avg'] = sum / len(chart_values)
                else:
                    res[key]['avg'] = 0
            else:
                res[key] = dict()
                res[key]['open'] = item['answer']
        return render_template('statistics.html', res=res, lang=session['lang'], quest=questions)


@app.route('/lang', methods=["POST"])
def set_lang():
    session['lang'] = request.form.get('lang')
    return redirect('/')


@app.route('/results')
@app.route('/results/')
def show_results():
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    else:
        res = getRawData()
        return render_template('results.html', res=res, lang=session['lang'])
