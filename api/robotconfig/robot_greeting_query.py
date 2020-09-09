# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_greeting_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotGreetingQuery:

    @staticmethod
    def greeting_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/greetingQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_normal_greeting_enable, re_normal_greeting_content, re_keyword_greeting_enable, \
                re_keyword_greeting_content, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["normalGreetingEnable"], result["bean"][
                        "normalGreetingContent"], result["bean"]["keywordGreetingEnable"], result["bean"][
                        "keywordGreetingContent"], result["bean"]["userId"]
                robot_id, normal_greeting_enable, normal_greeting_content, \
                keyword_greeting_enable, keyword_greeting_content, user_id = list(
                    SqlConnect(
                        "kicp_robot_config").exec_sql(
                        assert_value.split("-")[1])[0])
                return [re_robot_id, re_normal_greeting_enable, re_normal_greeting_content, re_keyword_greeting_enable,
                        re_keyword_greeting_content, re_user_id], [str(robot_id),
                                                                   True if normal_greeting_enable == 1 else False,
                                                                   normal_greeting_content,
                                                                   True if keyword_greeting_enable == 1 else False,
                                                                   keyword_greeting_content, str(user_id)]
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

#
# if __name__ == '__main__':
#     actual_result, expect_result = RobotGreetingQuery().greeting_query("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "709", "userId": "11"}),
#                                                                        "sql-select robotId,normalGreetingEnable,normalGreetingContent,keywordGreetingEnable,keywordGreetingContent,userId from robot_greeting_word where robotId=709")
#     print(actual_result, expect_result )
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
