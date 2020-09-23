# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_warm_word_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotWarmWordQuery:

    @staticmethod
    def warm_word_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/warmWordsQuery"
        warm_word_list = []
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_warm_response_enable, re_get_contact_dont_send_enable, \
                re_warm_send_limit_enable, re_warm_send_limit_nums, re_warm_word_list, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["warmResponseEnable"], result["bean"][
                        "getContactDontSendEnable"], result["bean"]["warmSendLimitEnable"], result["bean"][
                        "warmSendLimitNums"], result["bean"]["warmWordList"], result["bean"][
                        "userId"]

                sql_result_list = SqlConnect("kicp_robot_config").exec_sql(assert_value.split("-")[1])
                for i in range(len(sql_result_list)):
                    # if sql_result_list[i][5] and sql_result_list[i][7]:
                    #     warm_word_list.append(
                    #         {'recordId': str(sql_result_list[i][5]), 'robotId': str(sql_result_list[i][6]),
                    #          'responseContent': str(sql_result_list[i][8]),
                    #          'indexNo': str(sql_result_list[i][9])})
                    # elif sql_result_list[i][7] is not None:
                    warm_word_list.append(
                        {'recordId': str(sql_result_list[i][5]), 'robotId': str(sql_result_list[i][6]),
                         'intervalSeconds': sql_result_list[i][7],
                         'responseContent': str(sql_result_list[i][8]),
                         'indexNo': str(sql_result_list[i][9])})
                robot_id = str(sql_result_list[0][0])
                warm_response_enable = True if sql_result_list[0][1] == 1 else False
                get_contact_dont_send_enable = True if sql_result_list[0][2] == 1 else False
                warm_send_limit_enable = True if sql_result_list[0][3] == 1 else False
                warm_send_limit_nums = sql_result_list[0][4]
                user_id = str(sql_result_list[0][10])
                return [re_robot_id, re_warm_response_enable, re_get_contact_dont_send_enable,
                        re_warm_send_limit_enable, re_warm_send_limit_nums, re_warm_word_list, re_user_id], \
                       [robot_id,
                        warm_response_enable,
                        get_contact_dont_send_enable,
                        warm_send_limit_enable,
                        warm_send_limit_nums,
                        warm_word_list,
                        user_id]
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
#     actual_result, except_result = RobotWarmWordQuery().warm_word_query("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "877", "userId": "11"}),
#                                                                         "sql-select ww.robotId,ww.warmResponseEnable,ww.getContactDontSendEnable,ww.warmResponseEnable,ww.warmSendLimitNums,wwl.recordId,wwl.robotId,wwl.intervalSeconds,wwl.responseContent,wwl.indexNo,ww.userId from robot_warm_word ww,robot_warm_word_list wwl where ww.robotId =877 and ww.userId = 11 and ww.userId = wwl.userId and wwl.robotId = ww.robotId")
#     print(actual_result)
#     print(except_result)
    # assert Assert.get_result(actual_result, except_result)
