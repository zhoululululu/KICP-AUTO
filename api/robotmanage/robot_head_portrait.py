# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_head_portrait.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from requests_toolbelt import MultipartEncoder
from commonfunc.assert_func import Assert

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotHeadPortrait:
    @staticmethod
    def head_portrait(url, params, assert_value):
        path = "/robotConfig/robotCfg/upload/headPortrait"
        data = MultipartEncoder(
            fields=[
                ("userId", json.loads(params)["userId"] if "userId" in params else ""),
                ("robotId", json.loads(params)["robotId"] if "robotId" in params else ""),
                ("file", (
                    json.loads(params)["head_portrait"] if "robotId" in params else "",
                    open(rootPath + "testdata\\robotmanage\\head_portrait.jpg", "rb"),
                    "image/jpeg"))
            ])

        header = {
            "Content-Type": data.content_type,
        }
        try:
            result = requests.post(url=url + path, data=data, headers=header).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

if __name__ == '__main__':
    actual_result, except_result = RobotHeadPortrait().head_portrait("https://tkf-kicp.kuaishang.cn",
                                                                     json.dumps({"userId": "11", "robotId": "358",
                                                                                 "head_portrait": "head_portrait.jpg"}),
                                                                     "code-8")
