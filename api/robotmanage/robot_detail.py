# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_detail.py
@author: ZL
@Desc  :
'''
import requests
from commonfunc.get_db_connect import SqlConnect
import json
import os
from commonfunc.assert_func import Assert

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotDetail:

    @staticmethod
    def detail_robot(url, params, assert_value):
        path = "/robotConfig/robotCfg/manage/details"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "sql" in assert_value and "bean" in result:
                re_robot_id, re_robot_name, re_nick_name_insite, re_robot_type, re_robot_package, re_robot_template, re_robot_status, re_add_time, re_user_id = \
                    result["bean"]["robotId"], result["bean"]["robotName"], result["bean"]["nickNameInsite"], \
                    result["bean"]["robotType"], result["bean"][
                        "robotPackage"], result["bean"]["robotTemplate"], result["bean"]["robotStatus"], \
                    result["bean"][
                        "addTime"], result["bean"]["userId"]
                robot_id, robot_name, nick_name_insite, robot_type, robot_package, robot_template, robot_status, add_time, user_id = list(
                    SqlConnect(
                        "kicp_robot_config").exec_sql(
                        assert_value.split("-")[1])[0])
                return (
                [re_robot_id, re_robot_name, re_nick_name_insite, re_robot_type, re_robot_package, re_robot_template,
                 re_robot_status, re_add_time, re_user_id],
                [str(robot_id), robot_name, nick_name_insite, robot_type, robot_package, robot_template, robot_status,
                 str(add_time),
                 str(user_id)])

            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            elif "code" in assert_value:
                code = result["code"]
                expect_data = assert_value.split("-")[1]
                return str(code), expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception


# if __name__ == '__main__':
#     message, except_data = actual_result, except_result = RobotDetail().detail_robot("https://tkf-kicp.kuaishang.cn",
#                                                                                      json.dumps(
#                                                                                          {"userId": 11,
#                                                                                           "robotId": 358}),
#                                                                                      "sql-select robotId,robotName,nickNameInsite,robotType,robotPackage,robotTemplate,robotStatus,addTime,userId from robot_basic_info where userId=11 and robotId=358")
#     print(message, except_data)
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
