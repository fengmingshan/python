from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class Form1(FlaskForm):
    name = StringField('name')
    submit1 = SubmitField('submit')

class Form2(FlaskForm):
    name = StringField('name')
    submit2 = SubmitField('submit')
