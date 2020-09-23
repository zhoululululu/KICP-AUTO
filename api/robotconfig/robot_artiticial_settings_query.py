# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_artiticial_settings_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotArtiticialSettingsQuery:

    @staticmethod
    def artiticial_settings_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/artificialQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params.encode("UTF-8"))).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "sql" in assert_value and "bean" in result:
                re_robot_id, re_guest_display_enable, re_guest_display_word, re_unknow_question_display_enable, \
                re_unkonw_question_count_times, re_unknow_question_display_word, re_unsolve_question_display_enable, \
                re_unsolve_question_display_word, \
                re_keyword_display_enable, re_keyword_content, re_keyword_exact_enable, re_keyword_display_word, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["guestDisplayEnable"], result["bean"][
                        "guestDisplayWord"], result["bean"]["unknowQuestionDisplayEnable"], result["bean"][
                        "unkonwQuestionCountTimes"], result["bean"]["unknowQuestionDisplayWord"], result["bean"][
                        "unsolveQuestionDisplayEnable"], result["bean"][
                        "unsolveQuestionDisplayWord"], result["bean"][
                        "keywordDisplayEnable"], result["bean"]["keywordContent"], result["bean"]["keywordExactEnable"], \
                    result["bean"][
                        "keywordDisplayWord"], result["bean"]["userId"]
                robot_id, guest_display_enable, guest_display_word, unknow_question_display_enable, \
                unkonw_question_count_times, unknow_question_display_word, unsolve_question_display_enable, \
                unsolve_question_display_word, \
                keyword_display_enable, keyword_content, keyword_exact_enable, keyword_display_word, user_id = list(
                    SqlConnect(
                        "kicp_robot_config").exec_sql(
                        assert_value.split("-")[1])[0])
                return [re_robot_id, re_guest_display_enable, re_guest_display_word, re_unknow_question_display_enable,
                        re_unkonw_question_count_times, re_unknow_question_display_word,
                        re_unsolve_question_display_enable, re_unsolve_question_display_word,
                        re_keyword_display_enable, re_keyword_content, re_keyword_exact_enable, re_keyword_display_word,
                        re_user_id], [
                           str(robot_id),
                           True if guest_display_enable == 1 else False, guest_display_word,
                           True if unknow_question_display_enable == 1 else False,
                           unkonw_question_count_times, unknow_question_display_word,
                           True if unsolve_question_display_enable == 1 else False,
                           unsolve_question_display_word,
                           True if keyword_display_enable == 1 else False, keyword_content,
                           True if keyword_exact_enable == 1 else False, keyword_display_word,
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
#     actual_result, expect_result = RobotArtiticialSettingsQuery().artiticial_settings_query(
#         "https://tkf-kicp.kuaishang.cn", json.dumps(
#             {"robotId": "760",
#              "userId": "11"}),
#         "sql-select robotId,guestDisplayEnable,guestDisplayWord,unknowQuestionDisplayEnable,unkonwQuestionCountTimes,unknowQuestionDisplayWord,unsolveQuestionDisplayEnable,unsolveQuestionDisplayWord,keywordDisplayEnable,keywordContent,keywordExactEnable,keywordDisplayWord,userId from robot_transfer_labor where robotId=760 and userId = 11")
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
#                                                                        "sql-select robotId,normalartiticial_settingsEnable,normalartiticial_settingsContent,keywordartiticial_settingsEnable,keywordartiticial_settingsContent,userId from robot_artiticial_settings_word where robotId=709")
#     print(actual_result, expect_result )
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
