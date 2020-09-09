# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_set_status.py
@author: ZL
@Desc  :
'''
import requests
from commonfunc.get_db_connect import SqlConnect
import json
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotSetStatus:

    @staticmethod
    def set_status_robot(url, params, assert_value):
        path = "/robotConfig/robotCfg/manage/startAndStop"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "message" in assert_value:
                re_bean = result["message"].strip()
                except_data = assert_value.split("-")[1]
                return re_bean, except_data
            else:
                return result, assert_value
        except Exception:
            raise Exception
