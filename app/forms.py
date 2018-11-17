from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired
from dbqueries import get_groups

class LoginForm(FlaskForm):
    login = StringField('login', validators = [InputRequired()])
    password = PasswordField('password', validators = [InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    login = StringField('login', validators = [InputRequired()])
    password = PasswordField('password', validators = [InputRequired()])
    passwordRepeat = PasswordField('passwordRepeat', validators = [InputRequired()])
    submit = SubmitField('Register')

class AddChildForm(FlaskForm):
    choices = get_groups()
    ch = []
    for item in choices:
        ch.append((item[0] , item[3] + ' '+ item[1]))
    name = StringField('name', validators = [InputRequired()])
    group = SelectField('group', choices=ch, validators = [InputRequired()])
    submit = SubmitField('Add')

class DeleteChildForm(FlaskForm):
    name = StringField('name', validators = [InputRequired()])
