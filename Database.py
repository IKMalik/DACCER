import sqlite3 as sq
import sys


#-------------BONUS------------#
# allow saving graphs to db for users
# multiple alt paths
# Agreegate sql functions - maybe count number users in database
# log out instead of end application

#---------- IMPROVEMENTS-------------#
# Could split program across multiple files
# change how dedault data runs

class Database:
    '''
            new_username = self.entry_user.get()
    new_password = self.entry_pass.get()
    self.database.enter_data(new_username, new_password)
    tk.messagebox.showinfo("Registered", "You have been registered and may now log in")
    '''
    def __init__(self):

        self.conn = sq.connect("Userdatabase.db")  # connections to database setup
        self.conn.execute("pragma foreign_keys")  # foreign keys enabled 
        self.c = self.conn.cursor()
        self.setup_table()  # creates tables in database if not already made
        #self.default_data_user()
        #self.default_data_admin()
        self.show_details()

    def setup_table(self):    # Method to create table if one does not exist

        self.c.execute("CREATE TABLE IF NOT EXISTS userinfo("

                       "userid TEXT NOT NULL PRIMARY KEY,"
                       " password TEXT,"
                       " name TEXT)")

        self.c.execute("CREATE TABLE IF NOT EXISTS admininfo("

                       "adminid TEXT NOT NULL PRIMARY KEY,"
                       "password TEXT,"
                       "user_id TEXT REFERENCES userinfo(userid))")

    def default_data_admin(self):
        import Encryption as encryp
        encryption = encryp.Mergesort()
        secure_admin_pass = encryption.encrypt_data('password')

        self.c.execute("INSERT INTO admininfo(adminid, password, user_id) VALUES (?, ?, ?)",
                       ('ikm', secure_admin_pass, 'james'))
        self.conn.commit()

    def default_data_user(self):
        import Encryption as encryp
        encryption = encryp.Mergesort()

        secure_pass = encryption.encrypt_data('bond')
        self.c.execute("INSERT INTO userinfo(userid, password, name) VALUES (?, ?, ?)",
                       ('james', secure_pass, 'jamie'))
        self.conn.commit()

    def enter_data(self, username, password):   # Method to allow user to register
        import Encryption as encryp
        encryption = encryp.Mergesort()
        secure_pass = encryption.encrypt_data(password)
        self.c.execute("INSERT INTO userinfo (userid, password) VALUES (?, ?)",(username,secure_pass))
        self.conn.commit()

    def check_user_login(self, username, password): # Method to validate user login inputs
        import Encryption as encryp
        encryption = encryp.Mergesort()
        valid = ""
        self.c.execute("SELECT password FROM userinfo WHERE userid = ?", (username,))
        stored_pass = self.c.fetchone()

        if stored_pass is None:
            return 'False'
        else:
            print(stored_pass)
            stored_pass = encryption.decrypt_data(stored_pass)
            if password == stored_pass:
                valid = "user"

        return valid

    def check_admin_login(self, username, password): # Method to validate user login inputs
        import Encryption as encryp
        encryption = encryp.Mergesort()
        valid = ""
        self.c.execute("SELECT password FROM admininfo WHERE adminid = ?", (username,))
        stored_pass = self.c.fetchone()

        if stored_pass is None:
            return 'False'
        else:
            stored_pass = encryption.decrypt_data(stored_pass)
            if password == stored_pass:
                valid = "admin"

        return valid

    def check_newuser(self, userid):

        self.c.execute("SELECT userid FROM userinfo WHERE userid = ?", (userid,))
        data = self.c.fetchone()
        if data is None:
            print('data is none')
            return True
        else:
            return False
    
    def update_user(self,userid ,newusername):
        self.c.execute("UPDATE userinfo SET userid='{}'".format(newusername)+"WHERE userid ='{}'".format(userid))
        self.conn.commit()

    def show_details(self):
        self.c.execute("SELECT user_id FROM admininfo")
        self.conn.commit()

    def remove_user(self, userid):
        self.c.execute("DELETE FROM userinfo WHERE userinfo.userid = (?)",(userid,))
        self.conn.commit()
    

