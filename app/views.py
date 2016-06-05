from app import app
from app.main.survey import Survey
from flask import render_template
from flask import request
from app.forms import SurveyForm


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = SurveyForm()
    print(form.questions,
          form.question,
          form.question_1,
          form.question_2,
          form.question_3,
          form.question_4,
          form.question_5
          )
    # for q in form.questions:
    #     form.add_elem(q.label, q)
    if form.validate_on_submit():
        print([question.data for question in form.questions])
        # return save_survey_data(form)
    else:
        print(form.errors)
    return render_template('index.html', form=form)


@app.route('/survey/')
def process_question():
    pass
# @app.route('/')
# def world():
#     user = {'nickname': 'You' }
#     return render_template("layout.html",
#                            title = 'World',
#                            user = user)


@app.route('/temp')
def temp():
    return "Temp"

# @app.route('/hash/<int:survey_hash>', methods=['POST'])
# def send_result(survey_hash):
#     pass
