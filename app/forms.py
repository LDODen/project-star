from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,  BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from dbqueries import get_groups, viewchildren


def get_groups_choices():
    choices = get_groups()
    ch = []
    for item in choices:
        ch.append((item[0] , item[3] + ' '+ item[1]))
    return ch

def get_user_childs(user_id):
    childs = viewchildren(user_id)
    ch = []
    for item in childs:
        ch.append((item[0], item[1]))
    return ch


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
    name = StringField('name', validators = [InputRequired()])
    group = SelectField('group', choices=get_groups_choices())
    submit = SubmitField('Add')


class DeleteChildForm(FlaskForm):
    name = StringField('name', validators = [InputRequired()])
    submit = SubmitField('Delete')


class AddDayForm(FlaskForm):
        
    childName = SelectField('Child name')
    date = DateField('Date', format='%Y-%m-%d')
    status = BooleanField('WasOrNot')
    submit = SubmitField('Add')
    
    def __init__(self, user_id, *args, **kwargs):
        super(AddDayForm, self).__init__(*args, **kwargs)
        self.childName.choices = get_user_childs(user_id)