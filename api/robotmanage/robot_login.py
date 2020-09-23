# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_login.py
@author: ZL
@Desc  :
'''
import requests
import os
from commonfunc.get_db_connect import SqlConnect
import time
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotLogin:
    @staticmethod
    def login_robot(url, params, assert_value):
        path = "/robotConfig/robotCfg/login"

        try:
            result = requests.get(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            if "sql" in assert_value and "bean" in result:
                re_user_id, re_username = result["bean"]["userInfo"]["userId"], result["bean"]["userInfo"]["userName"]
                user_id, username = list(
                    SqlConnect(
                        "kicp_user_manage").exec_sql(
                        assert_value.split("-")[1])[0])
                return [re_user_id, re_username], [str(user_id), username]
            else:
                return result, assert_value
        except Exception:
            raise Exception

# if __name__ == '__main__':
#     actual_result, except_result = RobotLogin().login_robot("https://tkf-kicp.kuaishang.cn",
#                                                             json.dumps({"username": "zl-test", "password": "admin"}),
#                                                             'sql-select DISTINCT userId,userName from kicp_user_manage.`user` where userId=11')
#     print(actual_result)
#     print(except_result)
#     assert Assert.get_result(actual_result, except_result)
