# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_guest_settings_query.py
@author: ZL
@Desc  :
'''
import requests
from commonfunc.assert_func import Assert
import json
import os
from api.robotconfig.robot_hot_question_query import RobotHotQuestionQuery
from api.robotconfig.robot_related_question_query import RobotRelatedQuestionQuery
from api.robotconfig.robot_want_toask_query import RobotWantToaskQuery

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotGuestSettingsQuery:

    @staticmethod
    def guest_settings_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/findRobotGuestSettings"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "multi" in assert_value:
                re_result = json.dumps(result["bean"])
                expect_result = RobotGuestSettingsQuery.get_gust_settings_query(params)
                return re_result, expect_result

            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_gust_settings_query(params):
        robot_id = json.loads(params).get("robotId")
        user_id = json.loads(params).get("userId")
        hot_question_result = RobotHotQuestionQuery.get_hot_question_query(
            "select hq.robotId,hq.hotQuestionEnable,hq.hotDataMode,hq.guideWord,hq.userId from robot_hot_question hq where hq.robotId ={} and hq.userId = {} ".format(
                robot_id, user_id))
        want_toask_result = RobotWantToaskQuery.get_want_toask_query(
            "select robotId,wantToAskEnable,guideWord,showNumberLimit,userId from robot_want_toask where robotId={} and userId = {}".format(
                robot_id, user_id))
        related_question_result = RobotRelatedQuestionQuery.get_related_question_query(
            "select robotId,relatedQuestionEnable,guideWord,showNumberLimit,userId from robot_related_question where robotId={} and userId = {}".format(
                robot_id, user_id))
        expect_result = {
            "robotId": robot_id,
            "hotQuestion": json.loads(hot_question_result),
            "wantToask": json.loads(want_toask_result),
            "relatedQuestion": json.loads(related_question_result),
            "userId": user_id
        }
        return json.dumps(expect_result)


#
# if __name__ == '__main__':
#     actual_result, expect_result = RobotGuestSettingsQuery().guest_settings_query("https://tkf-kicp.kuaishang.cn",
#                                                                                   json.dumps(
#                                                                                       {"robotId": "877",
#                                                                                        "userId": "11"}), "multi-assert")
#     print(actual_result)
#     print(expect_result)
#
#     assert Assert.get_result(actual_result, expect_result)
