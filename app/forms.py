from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    login = StringField('login', validators = [InputRequired()])
    password = PasswordField('password', validators = [InputRequired()])

class RegisterForm(FlaskForm):
    login = StringField('login', validators = [InputRequired()])
    password = PasswordField('password', validators = [InputRequired()])
    passwordRepeat = PasswordField('passwordRepeat', validators = [InputRequired()])

class AddChildForm(FlaskForm):
    name = StringField('name', validators = [InputRequired()])
    group = StringField('group', validators = [InputRequired()])

class DeleteChildForm(FlaskForm):
    name = StringField('name', validators = [InputRequired()])
