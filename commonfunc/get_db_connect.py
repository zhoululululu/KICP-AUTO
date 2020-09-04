# -*- coding: UTF-8 -*-
'''
Created on 2020/9/4 17:56
@File  : get_db_connect.py
@author: ZL
@Desc  :
'''
from commonfunc.get_config import Config
import pymysql


class SqlConnect:
    def __init__(self, ):
        self.config = Config()
        self.c = self.config.get_sql_info()
        self.db_host = self.c["db_host"]
        self.db_port = int(self.c["db_port"])
        self.db_user = self.c["user_name"]
        self.db_password = self.c["user_pwd"]
        self.db_name = self.c["db_name"]

    def open(self):
        try:
            conn = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                db=self.db_name,
                port=self.db_port,
            )
        except pymysql.err.OperationalError as e:
            print("数据库连接失败！")
            raise
        self.currentConn = conn  # 数据库连接完成
        self.cursor = self.currentConn.cursor()  # 游标，用来执行数据库

    def exec_sql(self, sql, numbers=True):
        '''执行sql,支持执行多条sql语句。'''
        self.open()
        sqllist = self.spliteSql(sql)  # 先处理传入的sql语句
        with self.cursor as my_cursor:
            for i in sqllist:
                try:
                    my_cursor.execute(i)  # 执行sql语句
                    if numbers == False:
                        self.resultlist = my_cursor.fetchone()  # 获取一行数据
                    if numbers == True:
                        self.resultlist = my_cursor.fetchall()  # 获取多行数据
                    self.currentConn.commit()  # 提交
                except pymysql.err.ProgrammingError as e:
                    print("SQL语句不合法!")
        if self.currentConn:
            self.close()
        return self.resultlist


    def close(self):  # 关闭连接
        if self.cursor:
            self.cursor.close()
        self.currentConn.close()


if __name__ == '__main__':
    SqlConnect().exec_sql("select * from cc_robotcfg")
