import sqlite3 as sq
import tkinter as tk
import tkinter.messagebox
import Encryption as encryp  # importing my encryption module

class Database:

    first_run = True  # class variable to check for initial run

    def __init__(self):

        self.conn = sq.connect("Database.db")  # connections to database setup
        self.conn.execute("pragma foreign_keys")  # foreign keys enabled
        self.c = self.conn.cursor()  # cursor setup
        self.setup_table()  # creates tables in database if not already made
        if self.first_run:  # if it is initial run
            self.default_data_admin()  # create default data
            self.first_run = False
        else:
            pass

    def setup_table(self):    # Method to create table if one does not exist

        self.c.execute("CREATE TABLE IF NOT EXISTS userinfo("

                       "userid TEXT NOT NULL PRIMARY KEY,"
                       "adminid TEXT NOT NULL REFERENCES admininfo(adminid), "
                       " password TEXT,"
                       " numlogin INTEGER)")

        self.c.execute("CREATE TABLE IF NOT EXISTS admininfo("

                       "adminid TEXT NOT NULL PRIMARY KEY,"
                       "adminname TEXT,"
                       "password TEXT)")

    def default_data_admin(self):  # Method for creating default data

        encryption = encryp.Encryption()
        secure_admin_pass = encryption.encrypt_data('password')  # encrypt default password

        self.c.execute("INSERT OR IGNORE INTO admininfo(adminid, adminname, password) VALUES (?, ?, ?)",
                       ('admin', 'defaultname', secure_admin_pass))
        self.conn.commit()

    def enter_newuser (self, username, password, adminid):   # Method to allow user to register

        encryption = encryp.Encryption()
        secure_pass = encryption.encrypt_data(password)  # encrypting user entered password
        if not secure_pass:  # if unable to encrypt (invalid data)
            tk.messagebox.showerror('Invalid password', "Please ensure correct data was entered")
        else:
            self.c.execute("INSERT INTO userinfo (userid, password, adminid, numlogin)"
                           " VALUES (?, ?, ?, ?)", (username, secure_pass, adminid, 0))
            tk.messagebox.showinfo('Added', 'New user has been added')
            self.conn.commit()

    def check_newuser(self, userid):  # Method to check if user can be added
        checkadminid_exists = self.check_adminid(userid)  # check adminid in use
        if not checkadminid_exists:  # adminid does not exist/ not in use
            self.c.execute("SELECT userid FROM userinfo WHERE userid = ?", (userid,))
            data = self.c.fetchone()
            if data is None:  # userid not in use so can be added
                return True
            else:
                return False
        else:
            return False

    def check_adminid(self, userid): # check if admin id exists
        self.c.execute("SELECT adminid FROM admininfo WHERE adminid=?", (userid,))
        isadminid = self.c.fetchone()
        if isadminid is None:  # no adminid exists
            return False
        else:
            return True  # admin id exists

    def update_logincounter(self, userid):  # Method to incrmiment logincounter for user
        self.c.execute("SELECT numlogin FROM userinfo WHERE userid=?", (userid,))
        count = self.c.fetchall()[0]  # removing element from tuple
        for item in count:
            count = item + 1  # set new value
        self.c.execute("UPDATE userinfo SET numlogin = ?  WHERE userid = ?", (count, userid ))
        self.conn.commit()

    def check_login(self, username, password): # Method to validate login type
        check_admin = self.check_admin_login(username, password)  # check if valid admin loggin in
        if check_admin:  # if admin
            return 'admin'
        else:
            # is now either user or invalid
            encryption = encryp.Encryption()
            self.c.execute("SELECT password FROM userinfo WHERE userid = ?", (username,))
            stored_pass = self.c.fetchone()

            if stored_pass is None:  # no userid exists (no password)
                return 'False'
            else:
                stored_pass = encryption.decrypt_data(stored_pass)  # decrypt password for userid
                if password == stored_pass:  # if valid password
                    self.update_logincounter(username)  # update user log in counter
                    return "user"
                else:
                    return 'False'

    def get_joins(self):  # Method to perform a join to get the admin name associated with each userid
        self.c.execute("SELECT u.userid, a.adminname "
                       "FROM userinfo as u "
                       "INNER JOIN admininfo as a "
                       "ON u.adminid = a.adminid")

        return self.c.fetchall()

    def enter_newadmin(self, adminid, name, password):  # Method adds new admin to database

        encryption = encryp.Encryption()
        secure_pass = encryption.encrypt_data(password)
        if not secure_pass:  # if invalid password given to new admin
            tk.messagebox.showerror('Invalid password', "Please ensure correct data was entered")
        else: # add data
            self.c.execute("INSERT INTO admininfo (adminid, adminname, password)"
                           " VALUES (?, ?, ?)", (adminid, name, secure_pass))
            tk.messagebox.showinfo('Added', 'New admin has been added')
            self.conn.commit()

    def check_admin_login(self, username, password): # Method to validate admin login inputs
        self.c.execute("SELECT password FROM admininfo WHERE adminid = ?", (username,))
        check_admin_pass = self.c.fetchone()

        if check_admin_pass is None: # no password (no valid adminid so password would be none)
            return False

        else:
            encryption = encryp.Encryption()
            check_admin_pass = encryption.decrypt_data(check_admin_pass)
            if password == check_admin_pass:  # if decrypted password matches entered password
                return True
            else:
                return False

    def get_numusers(self): # Method to get number users in system
        self.c.execute("SELECT count(userid) FROM userinfo")
        return self.c.fetchone()

    def get_numadmins(self):  # Method to get number admins in system
        self.c.execute("SELECT count(adminid) FROM admininfo")
        return self.c.fetchone()

    def remove_user(self, userid):  # Method to remove users in system
        self.c.execute("DELETE FROM userinfo WHERE userinfo.userid = (?)", (userid,))
        self.conn.commit()

    def remove_admin(self, adminid):   # Method to remove admins in system
        self.c.execute("DELETE FROM admininfo WHERE adminid = (?)",(adminid,))
        self.conn.commit()
        self.remove_associatedusers(adminid)  # remove users associated with adminId
        self.check_noneadmins()  # check if all admins are removed (prevents system lockout)

    def check_noneadmins(self): # method to check if all admins are deleted and then add default

        self.c.execute("SELECT count(adminid) FROM admininfo")
        nbadmins = list(self.c.fetchone())[0] # removing data from tuple
        if nbadmins == 0:
            self.default_data_admin()  # if all admins delted add default admin

    def remove_associatedusers(self, adminid): # Method to remove users tied to adminid
        self.c.execute("DELETE FROM userinfo WHERE adminid= (?)", (adminid,))
        self.conn.commit()

    def getmostlogin(self, listy=None):  # Method to get three users with most logins in system

        if listy is None: # if no users have yet been added
            self.c.execute("SELECT userid, MAX(numlogin) FROM userinfo")
            userid = self.c.fetchone()[0]
            listy = [userid]
            self.getmostlogin(listy)  # recursively call method again

        elif len(listy) == 3: # three users been found (None added if less three users in system along with other users)
            tk.messagebox.showinfo("Users with most logins in system", listy)

        else:
            sql = 'SELECT userid, MAX(numlogin) FROM userinfo WHERE userid NOT in ({})'.format(
                ', '.join('?' for _ in range(len(listy))))
            self.c.execute(sql, listy)
            userid = self.c.fetchone()[0]
            listy.append(str(userid))
            self.getmostlogin(listy)  # recursively call method again
