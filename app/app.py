from datetime import datetime, date, timedelta
from flask import Flask, render_template, redirect, session, url_for, request, g
#from flask_login import current_user#login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from forms import LoginForm, RegisterForm, AddChildForm, DeleteChildForm, AddChildForm, AddDayForm, TabelForm, PricesForm, SchoolForm, GroupsForm, AccountsForm, PaymentsForm
from dbqueries import dbq
from passw import hash_password, check_password

app = Flask(__name__)
app.config.from_object('config')
ctx = app.app_context()
ctx.push()

def get_last_monthday(now):
    selected_date = date(datetime.now().year, datetime.now().month, datetime.now().day)
    if selected_date.month == 12: # December
        last_day_selected_month = date(selected_date.year, selected_date.month, 31) #.strftime("%Y-%m-%d")
    else:
        last_day_selected_month = date(selected_date.year, selected_date.month + 1, 1) - timedelta(days=1) #.strftime("%Y-%m-%d")
    return last_day_selected_month

def get_first_monthday(now):
    selected_date = date(datetime.now().year, datetime.now().month, 1)
    return selected_date #.strftime("%Y-%m-%d")

@app.before_request
def before_request():
    if (hasattr(g, "user")):
        pass
    else:
        g.user = ""
    if not (hasattr(g, 'db')):
        g.db = dbq("baseStar.db")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if (g.user != ""):
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = g.db.getuserbylogin(login_form.login.data)
        if (user != None):
            #print(user[2])
            if check_password(user[2], login_form.password.data):
                g.user = user
                session["User"] = user
                return redirect(url_for("index")) #"submitted!"
    return render_template("login.html", form = login_form)


@app.route("/register", methods = ["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = g.db.getuserbylogin(register_form.login.data)
        if(user is not None):
            return render_template('register.html', form = register_form)
        else:
            # TODO: сделать проверку совпадения паролей (как вариант сделать ее потом на javascript)
            hp = hash_password(register_form.password.data)
            g.db.insertuser(register_form.login.data, hp)
            user = g.db.getuserbylogin(register_form.login.data)
            g.user = user
            session["User"] = user
            return redirect(url_for("index"))
    return render_template('register.html', form = register_form)

@app.route("/index")
@app.route("/")
def index():
    #user = g.user
    #print(g.user)
    #print("2", session["User"])
    if "User" in session:
        if (session["User"] != ""):

            children = g.db.viewchildren(session["User"][0])
            tab = []
            for ch in children:
                #tab.append([ch, g.db.get_child_tabel(ch[0], get_first_monthday(datetime.now()), get_last_monthday(datetime.now()))])
                rows = g.db.get_tabel_with_prices(
                        ch[0], get_first_monthday(datetime.now()),
                        get_last_monthday(datetime.now()))

                price_sum = 0
                for row in rows:
                    price_sum = price_sum + row[4]

                tab.append([
                    ch,
                    rows,
                    price_sum,
                    len(rows)
                ])

        else:
            children = []
            tab = []
    else:
        session["User"] = ""
        children = []
        tab = []
    return render_template("index.html", user = session["User"], children = children, tabel = tab)

@app.route("/tabel/<childid>", methods = ["GET", "POST"])
def tabel(childid):
    tabel_form = TabelForm()
    if tabel_form.date_from.data == None:
        tabel_form.date_from.data = get_first_monthday(datetime.now())
        tabel_form.date_till.data = get_last_monthday(datetime.now())

    if request.method == "POST":
        date_begin = request.form['date_from']
        date_end = request.form['date_till']
        if "User" in session:
            if (session["User"] != ""):
                tab = []
                rows = g.db.get_tabel_with_prices(childid, date_begin, date_end)
                price_sum = 0
                for row in rows:
                    price_sum = price_sum + row[4]

                tab = [childid,
                        rows,
                        price_sum, len(rows)]
            else:
                tab = []
            return render_template("tabel.html", tabel = tab, form = tabel_form)  #,user = session["User"]
        else:
            return redirect(url_for("login"))
    tab = []
    rows = g.db.get_tabel_with_prices(childid, tabel_form.date_from.data,
                                   tabel_form.date_till.data)
    price_sum = 0
    for row in rows:
        price_sum = price_sum + row[4]

    tab = [childid, rows, price_sum, len(rows)]
    return render_template("tabel.html", tabel = tab, form = tabel_form)

@app.route("/logout")
def logout():
    g.user = ""
    session["User"] = ""
    return redirect(url_for("index"))


@app.route("/prices", methods = ["GET", "POST"])
def prices():
    prices_form = PricesForm()
    if request.method == "POST":
        g.db.add_price(prices_form.price_date.data, prices_form.group_name.data, prices_form.date_sum.data)
        return redirect(url_for("prices"))
    return render_template("prices.html", form = prices_form)


@app.route("/addch", methods = ["GET", "POST"])
def addch():
    add_child_form = AddChildForm()
    if request.method == "POST":
        us = session["User"]
        chname = request.form['name']
        group = request.form['group']
        g.db.add_child(chname, us[0], group)
        return redirect(url_for("index"))
        # тут почему-то не срабатывает валидация формы и сабмит
        # пришлось переделать через request.method
        # TODO: надо разобраться, может попробовать form.validate()
        #if add_child_form.validate_on_submit():
    return render_template('addchild.html', form = add_child_form)

@app.route("/deletech", methods=["GET","POST"])
def deletech():
    del_child_form = DeleteChildForm()
    if del_child_form.validate_on_submit():
        #print(del_child_form.name.data)
        #print(session["User"][0])
        g.db.delete_child(del_child_form.name.data, session["User"][0])
    return render_template('deletechild.html', form = del_child_form)

@app.route("/addday", methods=["GET", "POST"])
def addday():
    us = session["User"]
    add_day_form = AddDayForm(us[0])
    #if add_day_form.validate():
    if request.method == "POST":
        g.db.add_day(add_day_form.date.data, add_day_form.childName.data, add_day_form.status.data)
        return redirect(url_for("index"))
    return render_template('addday.html', form = add_day_form)

#
#
#
@app.route("/schools", methods=["GET", "POST"])
def schools():
    add_school_form = SchoolForm()
    if request.method == "POST":
        chname = request.form['name']
        g.db.add_school(chname,
                        'add' if add_school_form.submitAdd.data else 'del')
        return redirect(url_for("index"))
    return render_template('addschool.html', form=add_school_form)


@app.route("/groups", methods=["GET", "POST"])
def groups():
    add_group_form = GroupsForm()
    school = ""
    if request.method == "POST":
        us = session["User"]
        group_name = request.form['name']
        school_id = request.form['school']
        g.db.add_group(group_name, school_id)
        return redirect(url_for("index"))
    return render_template('addgroup.html', form=add_group_form, par=school)


@app.route("/accounts", methods=["GET", "POST"])
def accounts():
    add_account_form = AccountsForm()
    if request.method == "POST":
        account_name = request.form['name']
        g.db.add_account(account_name)
        return redirect(url_for("index"))
    accounts_list = g.db.get_accounts()
    return render_template('addaccounts.html', form=add_account_form, acc = accounts_list)

if (__name__ == '__main__'):
    app.run(debug=True)
