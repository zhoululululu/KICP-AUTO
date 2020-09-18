# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_related_question_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotRelatedQuestionQuery:

    @staticmethod
    def related_question_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/relatedQuestionQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                expect_result = assert_value.split("-")[1]
                return re_code, expect_result

            elif "sql" in assert_value and "bean" in result:
                re_result = json.dumps(result["bean"])
                expect_result = RobotRelatedQuestionQuery.get_related_question_query(assert_value.split("-")[1])
                return re_result, expect_result
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_related_question_query(sql):
        query_result = {}
        robot_id, related_question_enable, guide_word, show_number_limit, user_id = list(
            SqlConnect(
                "kicp_robot_config").exec_sql(sql)[0])
        if robot_id:
            query_result = {
                "robotId": str(robot_id), "relatedQuestionEnable": True if related_question_enable == 1 else False,
                "guideWord": guide_word,
                "showNumberLimit": show_number_limit, "userId": str(user_id)
            }
        return json.dumps(query_result)


#
# if __name__ == '__main__':
#     actual_result, expect_result = RobotRelatedQuestionQuery().related_question_query("https://tkf-kicp.kuaishang.cn",
#                                                                                       json.dumps(
#                                                                                           {"robotId": "760",
#                                                                                            "userId": "11"}),
#                                                                                       "sql-select robotId,relatedQuestionEnable,guideWord,showNumberLimit,userId from robot_related_question where robotId=760 and userId = 11")
#     print(actual_result)
#     print(expect_result
