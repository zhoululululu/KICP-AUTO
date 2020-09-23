# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_hot_question_save.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotHotQuestionSave:

    @staticmethod
    def hot_question_save(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/hotQuestionSave"
        header = {
            "Content-Type": "application/json"
        }
        try:
            result = requests.post(url=url + path, data=params.encode('utf-8'), headers=header).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception


# if __name__ == '__main__':
#     actual_result, expect_result= RobotHotQuestionSave.hot_question_save("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId":"877","hotQuestion":{"robotId":"877","hotQuestionEnable":"false","hotDataMode":"MANUAL_ADD","guideWord":"测试热点问题","hotQuestionList":[{"id":"101305312947044352","question":"zl-test分类测试问题1","similarQuestionCount":1,"effectiveType":0,"userId":"11","robotId":"877","modifyTime":"2020-09-17 23:56:21","key":"101305312947044352","isFind":"true","faqId":"101305312947044352","hotDataMode":"MANUAL_ADD"}]},"userId":"11"}), "code-8")
#     print(actual_result, expect_result)
    # assert Assert.get_result(actual_result, except_result)
