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

    def get_tabel_with_prices(self, child_id, date_from, date_to):
        query = r"""select tabel.date, tabel.childid, tabel.value, max(pric.price_date), pric.price, chil.name, chil.userid, chil.groupid from tabel
        left join children chil on childid = chil.id, 
        (Select price_date, price, groupid from prices) pric on date >= pric.price_date and chil.groupid = pric.groupid
        where tabel.value = 1 and tabel.childid = ? and tabel.date between date(?) and date(?)
        group by tabel.date, tabel.childid, chil.userid, chil.groupid"""

        self.cur.execute(query, (child_id, date_from, date_to, ))
        rows = self.cur.fetchall()
        return rows

    def get_price(self, price_date, child_id):
        query = r"""select chil.id, chil.name, chil.userid, pr1.groupid, pr1.price_date, pr1.price from children chil
        left join (select pr.id, pr.groupid, pr.price_date, pr.price from (
        select max(price_date) maxdate
        from prices
        where price_date<=?
        group by groupid) maxdates
        left join prices pr on maxdates.maxdate = pr.price_date
        group by groupid) pr1 on chil.groupid = pr1.groupid
        where chil.id = ?  """

        self.cur.execute(query, (price_date, child_id, ))
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

    def add_price(self, date, group_id, price):
        self.cur.execute(r"SELECT * from prices where price_date = date(?) and groupid = ?", (date, group_id, ))
        rows = self.cur.fetchall()
        if len(rows):
            self.cur.execute(
                r"UPDATE prices set price = ? where price_date = date(?) and groupid = ? ", (price, date, group_id, ))
        else:
            self.cur.execute(r"INSERT into prices VALUES (NUll, date(?), ?, ?)", (date, price, group_id,))
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

    def get_schools(self):
        self.cur.execute(r"SELECT * from school")
        rows = self.cur.fetchall()
        return rows

    def add_school(self, name, param):
        if param == "add":
            self.cur.execute(r"INSERT into school VALUES (NUll, ?)", (name, ))
            self.conn.commit()
        else:
            self.cur.execute(r"DELETE FROM school WHERE name=?", (name,))
            self.conn.commit()

    def add_group(self, group_name, school_id):
        self.cur.execute(r"SELECT * FROM groups WHERE name=? and schoolid=?", (group_name, school_id))
        rows = self.cur.fetchall()
        if (len(rows) > 0):
            return None
        else:
            self.cur.execute(r"INSERT INTO groups VALUES (NUll, ?, ?)", (group_name, school_id))
            self.conn.commit()

    def get_accounts(self):
        self.cur.execute(r"SELECT * from accounts")
        rows = self.cur.fetchall()
        return rows
    
    def add_account(self, account_name):
        pass