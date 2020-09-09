# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_greeting_save.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotGreetingsave:

    @staticmethod
    def greeting_save(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/greetingSave"
        header = {
            "Content-Type": "application/json"
        }
        try:
            result = requests.post(url=url + path, data=params, headers=header).json()
            print(result)
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


#
# if __name__ == '__main__':
#     actual_result, expect_result = RobotGreetingsave().greeting_save("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"robotId": "709", "normalGreetingEnable": "true",
#          "normalGreetingContent": "<div>zl-专用查询机器人配置（非空）-通用问候语内容A</div>", "keywordGreetingEnable": "false",
#          "keywordGreetingContent": "<div>zl-专用查询机器人配置（非空）-关键词问候语内容A</div>", "userId": "11"}), "code-8")
    #     print(actual_result, expect_result )
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
