import sqlite3
import config

db_name = "baseStar.db"

# TODO: переделать как класс с одним коннектом при инициализации
# TODO: засунуть connect в app.before_request и сохранять объект с подключением глобально в сессии

def insertuser(login, password):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"INSERT into Users VALUES (NUll, ?, ?)", (login, password,))
    conn.commit()
    conn.close()

def viewchildren(user_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"SELECT * FROM children WHERE userid = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def getuserbylogin(user_login):
    #print(user_login)
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"SELECT * FROM Users WHERE login = ?", (user_login,))
    rows = cur.fetchall()
    conn.close()
    if (len(rows) > 0):
        return rows[0]
    else: return None    

def delete_child(name, userid):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"DELETE FROM children WHERE name=? and userid=?", (name, userid,))
    #cur.execute("DELETE FROM children WHERE name = ?", (name,))
    cur = conn.cursor()
    conn.commit()
    conn.close()

def get_groups():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"select groups.*, school.name as school_name from groups left join school on groups.schoolid = school.id")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_child(child_name, user_id, group_id):
    print(child_name, user_id,group_id, sep=';')
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(r"INSERT into children VALUES (NUll, ?, ?, ?)", (child_name, user_id, group_id,))
    conn.commit()
    conn.close()


#def update(q,p,i):
#    conn = sqlite3.connect("lite.db")
#    cur = conn.cursor()
#    cur.execute("UPDATE store SET quantity=?, price=? where item=?", (q,p,i))wwww
#    conn.commit()
#    conn.close()

