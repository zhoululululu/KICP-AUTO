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
    def __init__(self, db_name):
        self.config = Config()
        self.c = self.config.get_sql_info()
        self.db_host = self.c["db_host"]
        self.db_port = int(self.c["db_port"])
        self.db_user = self.c["user_name"]
        self.db_password = self.c["user_pwd"]
        self.db_name = db_name

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

    def spliteSql(self, sql):
        sqllist = sql.split(';')
        return sqllist[0:-1]
        # 最后面会多一条空值

    def exec_sql(self, sql):
        '''执行sql,支持执行多条sql语句。'''
        self.open()
        with self.cursor as my_cursor:
            my_cursor.execute(sql)  # 执行sql语句
            self.resultlist = my_cursor.fetchall()
            return self.resultlist

    def delete_data(self, sql):
        self.open()
        with self.cursor as my_cursor:
            my_cursor.execute(sql)  # 执行删除
            # 提交
            self.currentConn.commit()

    def close(self):  # 关闭连接
        if self.cursor:
            self.cursor.close()
        self.currentConn.close()


#
# if __name__ == '__main__':
#     result = SqlConnect("kicp_robot_config").exec_sql(
#         "select gw.robotId,gw.guideResponseEnable,gwl.recordId,gw.robotId,gwl.intervalSeconds,gwl.indexNo,gw.userId from robot_guide_word gw,robot_guide_word_list gwl where gw.robotId =709 and gw.userId = 11 and gw.userId = gwl.userId and gwl.robotId = gw.robotId")
#     print(result)
