# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_un_problem_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotUnProblemQuery:

    @staticmethod
    def un_problem_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/unProblemQuery"
        unknow_response_list = []
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_unknow_response_enable, re_delay_seconds_from, \
                re_delay_seconds_to, re_unknow_response_list, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["unknowResponseEnable"], result["bean"][
                        "delaySecondsFrom"], result["bean"]["delaySecondsTo"], result["bean"][
                        "unknowResponseList"], result["bean"][
                        "userId"]
                sql_result_list = SqlConnect("kicp_robot_config").exec_sql(assert_value.split("-")[1])
                for i in range(len(sql_result_list)):
                    unknow_response_list.append(
                        {'recordId': str(sql_result_list[i][4]), 'robotId': str(sql_result_list[i][5]),
                         'responseContent': sql_result_list[i][6],
                         'indexNo': str(sql_result_list[i][7])})
                robot_id = str(sql_result_list[0][0])
                unknow_response_enable = True if sql_result_list[0][1] == 1 else False
                delay_seconds_from = sql_result_list[0][2]
                delay_seconds_to = sql_result_list[0][3]
                user_id = str(sql_result_list[0][8])
                return [re_robot_id, re_unknow_response_enable, re_delay_seconds_from, \
                        re_delay_seconds_to, re_unknow_response_list, re_user_id], \
                       [robot_id, unknow_response_enable, delay_seconds_from, \
                        delay_seconds_to, unknow_response_list, user_id]
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
#     actual_result, except_result = RobotUnProblemQuery().un_problem_query("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "709", "userId": "11"}),
#                                                                           "sql-select up.robotId,up.unknowResponseEnable,up.delaySecondsFrom,up.delaySecondsTo,upl.recordId,upl.robotId,upl.responseContent,upl.indexNo,up.userId from robot_unknow_response up,robot_unknow_response_list upl where up.robotId =709 and up.userId = 11 and up.userId = upl.userId and upl.robotId = up.robotId")
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
