from flask import Flask, render_template, redirect, session, url_for, request, g
#from flask_login import current_user#login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from forms import LoginForm, RegisterForm, AddChildForm, DeleteChildForm, AddChildForm, AddDayForm
#from dbqueries import insertuser, getuserbylogin, viewchildren, delete_child, add_child, add_day, get_child_tabel, dbq
from dbqueries import dbq
from passw import hash_password, check_password

app = Flask(__name__)
app.config.from_object('config')
ctx = app.app_context()
ctx.push()


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
                tab.append([ch, g.db.get_child_tabel(ch[0], '2018-09-01', '2018-12-31')])
        else:
            children = []    
            tab = []
    else:
        session["User"] = ""
        children = []
        tab = []        
    return render_template("index.html", user = session["User"], children = children, tabel = tab)

@app.route("/logout")    
def logout():
    g.user = ""
    session["User"] = ""
    return redirect(url_for("index"))

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

if (__name__ == '__main__'):
    app.run(debug=True)

