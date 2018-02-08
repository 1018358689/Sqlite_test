#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sqlite3


class db_demo():
    def __init__(self, db):
        self.db = db

    def create_db(self):
        conn = sqlite3.connect(self.db)
        # conn.execute('DROP TABLE USERS;')
        conn.execute(
            'CREATE TABLE IF NOT EXISTS USERS(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, AGE INT NOT NULL, SEX CHAR(10),CITY CHAR(30),SALARY REAL);')
        conn.execute('INSERT INTO USERS (ID,NAME,AGE,SEX,CITY,SALARY)'
                     'VALUES(1, "Leo", 32, "Female", "ShangHai", 12000)')
        conn.execute('INSERT INTO USERS (ID,NAME,AGE,SEX,CITY,SALARY)'
                     'VALUES(2, "Jack", 31, "Male", "BeiJing", 15000)')
        conn.commit()
        conn.close()

    def read_db(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM USERS')
        values = cur.fetchall()
        for row in values:
            print(row)
        cur.close()
        conn.close()

    def insert_db(self, str_list):
        conn = sqlite3.connect(self.db)
        conn.execute('INSERT INTO USERS (ID,NAME,AGE,SEX,CITY,SALARY)'
                     'VALUES({}, "{}", {}, "{}", "{}", {})'.format(str_list[0], str_list[1], str_list[2], str_list[3],
                                                             str_list[4], str_list[5]))
        conn.commit()
        conn.close()

    def update_db(self):
        conn = sqlite3.connect(self.db)
        conn.execute('UPDATE USERS SET SALARY = 3000 WHERE ID =2')
        conn.commit()
        conn.close()

    def select_db(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM USERS WHERE AGE > 30 AND SEX = "Female"')
        values = cur.fetchall()
        for row in values:
            print(row)
        cur.close()
        conn.close()

    def sort_db(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM USERS ORDER BY SALARY DESC')
        values = cur.fetchall()
        for row in values:
            print(row)
        cur.close()
        conn.close()

    def del_db(self, id):
        conn = sqlite3.connect(self.db)
        conn.execute('DELETE FROM USERS WHERE ID = {}'.format(id))
        conn.commit()
        conn.close()

# create_db('test001.db')
# read_db('test001.db')
if __name__ == '__main__':
    db1 = db_demo('test002.db')
    # db1.create_db()
    # db1.read_db()

    # str_list = [3,'Tom',33,'Female','ZheJiang',16000]
    # db1.insert_db(str_list)
    # db1.read_db()

    # db1.update_db()
    # db1.read_db()

    # db1.select_db()

    # db1.sort_db()

    # db1.del_db(3)
    # db1.read_db()