from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms import RadioField, TextAreaField, SelectMultipleField, widgets
from app.main.survey import Survey
import os


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiRadioField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.RadioInput()


class SurveyForm(Form):
    survey = Survey(os.path.join('app',
                                 'data',
                                 'questions.json'))
    questions = list()
    for q in sorted(survey.questions, key=lambda x: x.id):
        # question = ''
        if q.type == 'num':
            question = RadioField(label=q.key,
                                  choices=[(var, str(var)) for var in range(int(q.min),
                                             int(q.max),
                                             int(q.step))
                                          ]
                                 )
        elif q.type == 'open':
            question = TextAreaField(label=q.key)
        elif q.type == 'mult':
            question = SelectMultipleField(label=q.key,
                                           choices=q.variants,
                                           option_widget=widgets.CheckboxInput()
                                          )
        questions.append(question)
    question_1 = questions[0]
    question_2 = questions[1]
    question_3 = questions[2]
    question_4 = questions[3]
    question_5 = questions[4]


    @classmethod
    def add_elem(cls, name, elem):
        setattr(cls, name, elem)
