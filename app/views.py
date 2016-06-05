from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import json
import os


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
