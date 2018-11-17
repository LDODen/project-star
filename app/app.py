from flask import Flask, render_template, redirect, session, url_for, request, g
#from flask_login import current_user#login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from forms import LoginForm, RegisterForm, AddChildForm, DeleteChildForm
from dbqueries import insertuser, getuserbylogin, viewchildren, delete_child
from passw import hash_password, check_password

app = Flask(__name__)
app.config.from_object('config')


@app.before_request
def before_request():
    if (hasattr(g, "user")):
        pass
    else:
        g.user = ""    


@app.route("/login", methods = ["GET", "POST"])
def login():
    if (g.user != ""):
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = getuserbylogin(login_form.login.data)
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
        user = getuserbylogin(register_form.login.data)
        if(user is not None):
            return render_template('register.html', form = register_form)
        else:
            hp = hash_password(register_form.password.data)
            insertuser(register_form.login.data, hp)
            user = getuserbylogin(register_form.login.data) 
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
            children = viewchildren(session["User"][0])
        else:
            children = []    
    else:
        session["User"] = ""
        children = []        
    return render_template("index.html", user = session["User"], children = children)

@app.route("/logout")    
def logout():
    g.user = ""
    session["User"] = ""
    return redirect(url_for("index"))

@app.route("/addch")    
def addch():
    add_child_form = AddChildForm()
    if add_child_form.validate_on_submit():
        pass
    return render_template('addchild.html', form = add_child_form)

@app.route("/deletech", methods=["GET","POST"])    
def deletech():
    del_child_form = DeleteChildForm()
    if del_child_form.validate_on_submit():
        #print(del_child_form.name.data)
        #print(session["User"][0])
        delete_child(del_child_form.name.data, session["User"][0])    
    return render_template('deletechild.html', form = del_child_form)

@app.route("/addday")    
def addday():
    return redirect(url_for("index"))

if (__name__ == '__main__'):
    app.run(debug=True)
