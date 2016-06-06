# encoding: utf-8
__author__ = 'luves'
__date__ = '05.06.16'


from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class TestForm(Form):
    text_field = TextField('test', validators=[Required])