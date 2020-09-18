# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_delete.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect
import openpyxl

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotDelete:
    @staticmethod
    def delete_robot(url, params, assert_value):
        path = "/robotConfig/robotCfg/manage/delete"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                if re_code == "8":
                    try:
                        # 针对delete额外操作：修改用例表,将deleteId重新从库中寻找
                        delete_id = SqlConnect("kicp_robot_config").exec_sql(
                            "select robotId from robot_basic_info where userId = 11 and robotId!=358 and robotId!=877 ORDER BY robotId DESC")[
                            0][0]
                        wb = openpyxl.load_workbook(rootPath + "testdata\\robotmanage\\robot_manage.xlsx")
                        sheet = wb["delete_data"]
                        RobotDelete.modify(sheet, '正常删除', '{ "userId": 11,"robotId":' + str(delete_id) + '}')
                        wb.save(rootPath + "testdata\\robotmanage\\robot_manage.xlsx")

                    except Exception as e:
                        print('修改表格出错！', '\n', e)

                    # 删除该测试账号下无用的账号,358为userId为11下的需要校验的robot manage，709用与查询robot config非空查询
                    SqlConnect("kicp_robot_config").delete_data(
                        "delete from robot_basic_info where userId=11 and robotId!=358 and robotId!=877 and robotId!=" + str(
                            delete_id))
                    print("删除成功")
                return re_code, except_data

            elif "message" in assert_value:
                re_bean = result["message"].strip()
                except_data = assert_value.split("-")[1]
                return re_bean, except_data
        except Exception:
            raise

    def modify(sheet, name, value):
        for index, row in enumerate(sheet.rows):
            if name == sheet['A' + str(index + 1)].value:
                sheet.cell(row=index + 1, column=2, value=value)

# if __name__ == '__main__':
#     actual_result, expect_result  = RobotDelete().delete_robot(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"id": "898"}
#                    ),
#         'code-8')
#     print(actual_result)
#     print(expect_result)
    # assert Assert.get_result(actual_result, expect_result)