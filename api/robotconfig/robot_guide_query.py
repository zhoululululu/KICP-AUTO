# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_guide_query.py
@author: ZL
@Desc  :
'''
import requests
import json
from commonfunc.get_db_connect import SqlConnect
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotGuideQuery:

    @staticmethod
    def guide_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/guideQuery"
        guide_word_list = []
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_guide_response_enable, re_guide_word_list, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["guideResponseEnable"], result["bean"][
                        "guideWordList"], result["bean"]["userId"]
                sql_result_list = SqlConnect("kicp_robot_config").exec_sql(assert_value.split("-")[1])
                for i in range(len(sql_result_list)):
                    if sql_result_list[i][4]:
                        guide_word_list.append(
                            {'recordId': str(sql_result_list[i][2]), 'robotId': str(sql_result_list[i][3]),
                             'intervalSeconds': sql_result_list[i][4],
                             'responseContent': str(sql_result_list[i][5]),
                             'indexNo': str(sql_result_list[i][6])})
                    else:
                        guide_word_list.append(
                            {'recordId': str(sql_result_list[i][2]), 'robotId': str(sql_result_list[i][3]),
                             'responseContent': str(sql_result_list[i][5]),
                             'indexNo': str(sql_result_list[i][6])})
                robot_id = str(sql_result_list[0][0])
                guide_response_enable = True if sql_result_list[0][1] == 1 else False
                user_id = str(sql_result_list[0][7])
                return [re_robot_id, re_guide_response_enable, re_guide_word_list, re_user_id], [robot_id,
                                                                                                 guide_response_enable,
                                                                                                 guide_word_list,
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
#     actual_result, except_result = RobotGuideQuery().guide_query("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "709", "userId": "11"}),
#                                                                  "sql-select gw.robotId,gw.guideResponseEnable,gwl.recordId,gw.robotId,gwl.intervalSeconds,gwl.responseContent,gwl.indexNo,gw.userId from robot_guide_word gw,robot_guide_word_list gwl where gw.robotId =709 and gw.userId = 11 and gw.userId = gwl.userId and gwl.robotId = gw.robotId")
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
