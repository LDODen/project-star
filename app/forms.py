from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,  BooleanField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from dbqueries import dbq #get_groups, viewchildren
from datetime import datetime, date, timedelta


def get_schools():
    db = dbq("baseStar.db")
    choices = db.get_schools()
    ch = []
    for item in choices:
        ch.append((item[0], item[1]))
    return ch


def get_groups_choices():
    db = dbq("baseStar.db")
    choices = db.get_groups()
    ch = []
    for item in choices:
        ch.append((item[0] , item[3] + ' '+ item[1]))
    return ch

def get_user_childs(user_id):
    db = dbq("baseStar.db")
    childs = db.viewchildren(user_id)
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
    name = StringField('Имя', validators = [InputRequired()])
    group = SelectField('Группа', choices=get_groups_choices())
    submit = SubmitField('Добавить')


class DeleteChildForm(FlaskForm):
    name = StringField('Имя ребенка', validators = [InputRequired()])
    submit = SubmitField('Удалить')


class AddDayForm(FlaskForm):
    childName = SelectField('Ребенок')
    date = DateField('Дата', format="%Y-%m-%d")
    status = BooleanField('Ходил в сад')
    submit = SubmitField('Добавить')

    def __init__(self, user_id, *args, **kwargs):
        super(AddDayForm, self).__init__(*args, **kwargs)
        self.childName.choices = get_user_childs(user_id)


class TabelForm(FlaskForm):
    date_from = DateField('Дата с', format="%Y-%m-%d")
    date_till = DateField('Дата по', format="%Y-%m-%d")
    submit = SubmitField('Показать')

class PricesForm(FlaskForm):
    group_name = SelectField('Группа', choices=get_groups_choices())
    price_date = DateField('Дата цены', format="%Y-%m-%d")
    date_sum = FloatField('Сумма', default = 0.0)
    submit = SubmitField('Установить')

class GroupsForm(FlaskForm):
    name = StringField('Наименование', validators=[InputRequired()])
    school = SelectField('Школа/сад/', choices=get_schools())
    submitAdd = SubmitField('Создать')


class SchoolForm(FlaskForm):
    name = StringField('Наименование', validators=[InputRequired()])
    submitAdd = SubmitField('Создать')
    submitDel = SubmitField('Удалить')


class AccountsForm(FlaskForm):
    name = StringField('Наименование', validators = [InputRequired()])
    submitAdd = SubmitField('Создать')
    submitDel = SubmitField('Удалить')


class PaymentsForm(FlaskForm):
    pass
