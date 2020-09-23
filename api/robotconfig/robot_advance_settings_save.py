# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_advance_settings_save.py
@author: ZL
@Desc  :
'''
import requests
import json
import os

from commonfunc.assert_func import Assert
from commonfunc.change_data_type import ChangeDataType
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotAdvanceSettingsSave:

    @staticmethod
    def advance_settings_save(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/advancedSave"
        header = {
            "Content-Type": "application/json"
        }
        try:
            result = requests.post(url=url + path, data=params.encode('utf-8'), headers=header, timeout=1000).json()
            requests.session().close()
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
    # actual_result, expect_result = RobotAdvanceSettingsSave().advance_settings_save("https://tkf-kicp.kuaishang.cn",
    #                                                                                 json.dumps(
    #                                                                                     {"robotId":"877","timeResponseType":1,"speedNonTextSeconds":"null","speedTextWordCount":"null","guestFeedbackDisplayEnable":"true","guestFeedbackSolveWord":"解决","guestFeedbackUnsolveWord":"未解决","userId":"11","loaded":"true","randomSecondsFrom":2,"randomSecondsTo":3}), "code-8")
    # print(actual_result, expect_result)
    #     assert Assert.get_result(actual_result, except_result)
