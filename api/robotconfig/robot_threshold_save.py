# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_threshold_save.py
@author: ZL
@Desc  :
'''
import requests
import json
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotThresholdSave:
    @staticmethod
    def threshold_save(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/thresholdRangeSave"
        header = {
            "Content-Type": "application/json"
        }
        try:
            result = requests.post(url=url + path, data=json.dumps(params), headers=header).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "bean" in assert_value:
                re_bean = result["bean"].strip()
                except_data = assert_value.split("-")[1]
                return re_bean, except_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

# if __name__ == '__main__':
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         {"nickNameInsite": "zltestrobot1", "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "code-8")
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
