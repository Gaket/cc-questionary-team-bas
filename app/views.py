from app import app
from flask import render_template

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/temp')
def temp():
    return "Temp"

# @app.route('/hash/<int:survey_hash>', methods=['POST'])
# def send_result(survey_hash):
#     pass