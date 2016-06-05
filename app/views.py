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
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form['username'] == 'admin' and \
                request.form['password'] == 'secret':
            session['admin'] = True
            return redirect(url_for('statistics.html'))


@app.route('/statistics')
def get_statistics():
    if not session['admin']:
        return redirect(url_for('login'))
    else:
        data = json.load(os.path.join('app',
                                      'data',
                                      'aggregated_data.json'))
        return render_template('statistics.html', data=data)
