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
        # aggregating
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
                sum_ = 0
                [chart_labels.append(x) for x in range(0, len(item['answer']))]
                res[key]['labels'] = chart_labels
                element_number = 0
                total_cnt = 0
                for val in item['answer']:
                    chart_values.append(float(val))
                    sum_ += float(val) * element_number
                    element_number += 1
                    total_cnt += float(val)
                res[key]['vals'] = chart_values
                if total_cnt > 0:
                    res[key]['avg'] = float(sum_ )/ total_cnt
                else:
                    res[key]['avg'] = 0
            elif questions[key].type == 'open':
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


@app.route('/stat_group')
@app.route('/stat_group/')
def show_group_stat():
    if 'admin' not in session:
        return redirect(url_for('check_login'))
    else:
        raw = getRawData()
        qs = getQuestionsFromJSON(QUESTIONS_ADDR, session['lang'], QUESTIONS_TO_STATISTICS)
        stat = list()
        # stat = [ {name: answer#1_name,
        #           results: [0,0,0,0,0,0,0],
        #           total: int,
        #           surveyed: int},
        #           comments: list of str ]
        for hash_, sur in raw.items():
            rec = dict()
            rec['result'] = list()
            rec['surveyed'] = 0
            rec['total'] = 0
            rec['comments'] = []
            for a in sur:
                # TODO: remove hardcode
                if a['question_id'] == 1:
                    rec['name'] = a['answer'][0]
                elif a['question_id'] == 8:
                    rec['comments'].append(a['answer'][0])
                else:
                    rec['result'].append(int(a['answer'][0]))
            rec['total'] = sum(rec['result'])
            if rec['name'] not in [r['name'] for r in stat]:
                rec['surveyed'] += 1
                stat.append(rec)
            else:
                for r in stat:
                    if r['name'] == rec['name']:
                        r['result'] = [float(sum(i)) / 2 for i in zip(r['result'], rec['result'])]
                        r['total'] = sum(r['result'])
                        r['surveyed'] += 1
                        # Something like this
                        r['comments'] += (rec['comments'])

            # r['comments']
        print(stat)
        return render_template('stat_group.html', stat=stat, lang=session['lang'])
