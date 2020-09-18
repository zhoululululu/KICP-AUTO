# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_want_toask_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

from commonfunc.assert_func import Assert

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotWantToaskQuery:

    @staticmethod
    def want_toask_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/wantToaskQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "sql" in assert_value and "bean" in result:
                re_result = json.dumps(result["bean"])
                expect_data = RobotWantToaskQuery.get_want_toask_query(assert_value.split("-")[1])
                return re_result, expect_data
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_want_toask_query(sql):
        query_result = {}
        robot_id, want_to_ask_enable, guide_word, show_number_limit, user_id = list(
            SqlConnect(
                "kicp_robot_config").exec_sql(sql)[0])
        if robot_id:
            query_result = {
                "robotId": str(robot_id), "wantToAskEnable": True if want_to_ask_enable == 1 else False,
                "guideWord": guide_word,
                "showNumberLimit": show_number_limit, "userId": str(user_id)
            }
        return json.dumps(query_result)


#
# if __name__ == '__main__':
#     actual_result, expect_result = RobotWantToaskQuery().want_toask_query("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "760", "userId": "11"}),
#                                                                           "sql-select robotId,wantToAskEnable,guideWord,showNumberLimit,userId from robot_want_toask where robotId=760 and userId = 11")
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)

#
