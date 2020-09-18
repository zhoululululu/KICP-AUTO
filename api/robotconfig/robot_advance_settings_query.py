# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_advance_settings_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotAdvanceSettingsQuery:

    @staticmethod
    def advance_settings_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/advancedQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            requests.session().close()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_time_response_type, re_random_seconds_from, re_random_seconds_to, \
                re_guest_feedback_display_enable, re_guest_feedback_solve_word, re_guest_feedback_unsolve_word, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["timeResponseType"], result["bean"][
                        "randomSecondsFrom"], result["bean"]["randomSecondsTo"], result["bean"][
                        "guestFeedbackDisplayEnable"], result["bean"]["guestFeedbackSolveWord"], result["bean"][
                        "guestFeedbackUnsolveWord"], result["bean"]["userId"]
                robot_id, time_response_type, random_seconds_from, random_seconds_to, \
                guest_feedback_display_enable, guest_feedback_solve_word, guest_feedback_unsolve_word, user_id = list(
                    SqlConnect(
                        "kicp_robot_config").exec_sql(
                        assert_value.split("-")[1])[0])
                return [re_robot_id, re_time_response_type, re_random_seconds_from, re_random_seconds_to, \
                        re_guest_feedback_display_enable, re_guest_feedback_solve_word, re_guest_feedback_unsolve_word,
                        re_user_id], [str(robot_id),
                                      time_response_type,
                                      random_seconds_from, random_seconds_to,
                                      True if guest_feedback_display_enable == 1 else False,
                                      guest_feedback_solve_word,
                                      guest_feedback_unsolve_word,
                                      str(user_id)]
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
    # result = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
    #                                       sheet_name="query_advance_settings")
    # # assert_value = result.assert_value.tolist()
    # # params = result.data.tolist()
    #
    # for i in range(len(result)):
    #     actual_result, except_result = RobotAdvanceSettingsQuery.advance_settings_query("https://tkf-kicp.kuaishang.cn",
    #                                                                                     result[i][1],
    #                                                                                     result[i][2])
    #     print(actual_result, except_result)
    #     assert Assert.get_result(actual_result, except_result)
        #     actual_result, expect_result = RobotAdvanceSettingsQuery().advance_settings_query("https://tkf-kicp.kuaishang.cn",
#                                                                                       json.dumps(
#                                                                                           {"robotId": "760",
#                                                                                            "userId": "11"}),
#                                                                                       "sql-select robotId,timeResponseType,randomSecondsFrom,randomSecondsTo,guestFeedbackDisplayEnable,guestFeedbackSolveWord,guestFeedbackUnsolveWord,userId from robot_advanced_settings where robotId=760 and userId = 11")
#     print(actual_result, expect_result)
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
