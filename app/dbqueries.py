import sqlite3
import config

db_name = "baseStar.db"

class dbq():
 
    def __init__(self, name):
        self.db_name = name 
        #"baseStar.db"
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):    
        self.conn.close()

    def get_child_tabel(self, child_id, date_from, date_to):
        self.cur.execute(r"SELECT * from tabel where date BETWEEN date(?) AND date(?) and childid = ? order by date", (date_from, date_to, child_id, ))
        rows = self.cur.fetchall()
        return rows

    def add_day(self, date, child_id, status):
        self.cur.execute(r"SELECT * from tabel where date = date(?) and childid = ?", (date, child_id, ))
        rows = self.cur.fetchall()
        if len(rows):
            self.cur.execute(r"UPDATE tabel set value = ? where date = date(?) and childid = ? ", (status, date, child_id,))
        else:    
            self.cur.execute(r"INSERT into tabel VALUES (date(?), ?, ?, NUll)", (date, child_id, status,))
        self.conn.commit()
        
    def get_groups(self):
        self.cur.execute(r"SELECT groups.*, school.name as school_name from groups left join school on groups.schoolid = school.id")
        rows = self.cur.fetchall()
        return rows

    def add_child(self, child_name, user_id, group_id):
        self.cur.execute(r"INSERT into children VALUES (NUll, ?, ?, ?)", (child_name, user_id, group_id,))
        self.conn.commit()
       
    def insertuser(self, login, password):
        self.cur.execute(r"INSERT into Users VALUES (NUll, ?, ?)", (login, password,))
        self.conn.commit()
        

    def viewchildren(self, user_id):
        self.cur.execute(r"SELECT * FROM children WHERE userid = ?", (user_id,))
        rows = self.cur.fetchall()
        return rows

    def getuserbylogin(self, user_login):
        self.cur.execute(r"SELECT * FROM Users WHERE login = ?", (user_login,))
        rows = self.cur.fetchall()
        if (len(rows) > 0):
            return rows[0]
        else: return None    

    def delete_child(self, name, userid):
        self.cur.execute(r"DELETE FROM children WHERE name=? and userid=?", (name, userid,))
        self.conn.commit()
        
