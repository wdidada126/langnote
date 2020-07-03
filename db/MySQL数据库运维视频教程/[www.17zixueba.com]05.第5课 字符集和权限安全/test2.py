# -*- coding: utf-8 -*-
#coding=utf-8
# Copyright (c) 2014. All rights reserved.
# 
# @Author:  wangheng(ziliang)
# @Date  :  07/1/2014
# @Email :  wangheng.king@gmail.com
# */

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

try:
    import MySQLdb
except Exception, e:
    print "--[FAIL][%s] Import MySQLdb lib failed. %s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), e)
    sys.exit()

class my_database:
    def __init__(self, host = None, port = None, user = None, password = None, db = None, charset = None):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__charset = charset

    def connect(self, host = None, port = None, user = None, password = None, db = None, charset = None):
        if host and len(host) > 0:
            self.__host = host
        if port and port > 0:
            self.__port = port
        if user and len(user) > 0:
            self.__user = user
        if password and len(password) > 0:
            self.__password = password
        if db and len(db) > 0:
            self.__db = db
        if charset and len(charset) > 0:
            self.__charset = charset
        #print "-------- %s %s %s %s %s"%(self.__host, self.__port, self.__user, self.__password, self.__db)
        try:
            conn = MySQLdb.connect(
                host = self.__host, 
                port = self.__port,
                user = self.__user,
                passwd = self.__password,
                db = self.__db,
                charset = self.__charset,
                connect_timeout = 200)
        except Exception,e:
            print "--[FAIL][%s] Connect to mysql host:%s,port:%s,user:%s,password:%s failed. Detail:%s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self.__host,self.__port,self.__user,self.__password,e)
            return None
        return conn

    def disconnect(self, conn):
        if conn:
            conn.close()
            conn = None

    def execute(self, conn, sql, flag = 0):
        cur = conn.cursor()
        result = None
        try:
            print "[DEBUG] sql: %s" %(sql)
            result = cur.execute(sql)
            conn.commit()
            if flag:
                result = cur.fetchall()
        except Exception, e:
            print "--[FAIL][%s] Execute sql: %s failed. detail:%s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),sql, e)
            cur.close()
            return result
        cur.close()
        return result


class test1:
    __host = "127.0.0.1"
    __port = 3306
    __user = "test"
    __password = "test"
    __db = "test"
    __inchar = "gbk"
    __outchar = "utf8"
    def __init__(self):
        self.__database = my_database()
        self.__conn = None
    def run(self):
        sql1 = "Insert into test.test values(1, '喜欢')".encode('utf8')
        sql2 = "Insert into test.test values(2, '不喜欢')".encode('utf8')
        sql3 = "select * from test.test where id = 1"
        sql4 = "select * from test.test where id = 2"
        self.__conn = self.__database.connect(self.__host, self.__port, self.__user, self.__password, self.__db, self.__inchar)
        self.__database.execute(self.__conn, sql1)
        res = self.__database.execute(self.__conn, sql3, 1)
        print "############ 1 ###########"
        if res:
            for i in res:
                print str(i[0]) + ", " + i[1]
        self.__database.disconnect(self.__conn)

        self.__conn = self.__database.connect(self.__host, self.__port, self.__user, self.__password, self.__db, self.__outchar)
        res = self.__database.execute(self.__conn, sql3, 1)
        print "############ 2 ###########"
        for i in res:
            print str(i[0]) + ", " + i[1]
        self.__database.disconnect(self.__conn)

        self.__conn = self.__database.connect(self.__host, self.__port, self.__user, self.__password, self.__db, self.__outchar)
        self.__database.execute(self.__conn, sql2)
        res = self.__database.execute(self.__conn, sql4, 1)
        print "############ 3 ###########"
        for j in res:
            print str(j[0]) + ", " + j[1]
        self.__database.disconnect(self.__conn)

        self.__conn = self.__database.connect(self.__host, self.__port, self.__user, self.__password, self.__db, self.__inchar)
        res = self.__database.execute(self.__conn, sql4, 1)
        print "############ 4 ###########"
        for j in res:
            print str(j[0]) + ", " + j[1]
        self.__database.disconnect(self.__conn)


if __name__ == '__main__' :
    t1 = test1()
    t1.run()



