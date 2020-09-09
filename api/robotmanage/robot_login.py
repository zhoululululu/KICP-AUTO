# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_login.py
@author: ZL
@Desc  :
'''
import requests
import os
from commonfunc.get_db_connect import SqlConnect
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotLogin:
    @staticmethod
    def login_robot(url, params, assert_value):
        path = "/robotConfig/robotCfg/login"

        try:
            result = requests.get(url=url + path, params=params).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            if "sql" in assert_value and "bean" in result:
                re_user_id, re_username, re_add_time, re_modify_time, re_data_status, = result["bean"]["userInfo"][
                                                                                            "userId"], \
                                                                                        result["bean"]["userInfo"][
                                                                                            "userName"], \
                                                                                        result["bean"]["userInfo"][
                                                                                            "addTime"], \
                                                                                        result["bean"]["userInfo"][
                                                                                            "modifyTime"], \
                                                                                        result["bean"]["userInfo"][
                                                                                            "dataStatus"]
                re_typeid, re_typename, re_add_time, re_modify_time, re_data_status = result["bean"]["robotType"][0][
                                                                                          "typeId"], \
                                                                                      result["bean"]["robotType"][0][
                                                                                          "typeName"], \
                                                                                      result["bean"]["robotType"][0][
                                                                                          "addTime"], \
                                                                                      result["bean"]["robotType"][0][
                                                                                          "modifyTime"], \
                                                                                      result["bean"]["robotType"][0][
                                                                                          "dataStatus"]
                user_id, username, add_time, modify_time, data_status, typeid, typename, add_time, modify_time, data_status = SqlConnect(
                    "kicp_robot_config").exec_sql(
                    assert_value.split("-")[1])
                return [re_user_id, re_username, re_add_time, re_modify_time, re_data_status, re_typeid, re_typename,
                        re_add_time, re_modify_time, re_data_status], [str(user_id), username, str(add_time),
                                                                       str(modify_time),
                                                                       True if data_status == 1 else False,
                                                                       typeid,
                                                                       typename, str(add_time), str(modify_time),
                                                                       True if data_status == 1 else False]
            else:
                return result, assert_value
        except Exception:
            raise Exception

# if __name__ == '__main__':
#     actual_result, except_result = RobotLogin().login_robot("https://tkf-kicp.kuaishang.cn",
#                                                             "username=zl-test&password=admin",
#                                                             "sql-select DISTINCT rb.userId,rb.userName,rb.addTime,rb.modifyTime,rb.dataStatus,ra.robotType,ry.typeName,ry.addTime,ry.modifyTime,ry.dataStatus from kicp_robot_config.robot_basic_info ra,kicp_user_manage.`user` rb,kicp_basic_data.robot_type ry where ra.userId=11 and ra.userId =rb.userId and ra.robotType=ry.typeId")
#     actual_result, except_result = RobotAdd().add_robot("https://tkf-kicp.kuaishang.cn", json.dumps(
#         { "robotTemplate": "3", "robotPackage": "1", "nickNameOutsite": "zltestrobot1",
#          "signature": "周璐测试机器人1", "userId": "11"}), "bean-对内昵称为空")
#     assert Assert.get_result(actual_result, except_result)
