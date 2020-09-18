# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_delete.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert

from commonfunc.get_db_connect import SqlConnect
import openpyxl

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqDelete:

    @staticmethod
    def faq_delete(url, params, assert_value):
        path = "/faqConfig/robotFAQ/delete"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                if re_code == "8":
                    try:
                        # 针对delete额外操作：修改用例表,将faqId重新从库中寻找
                        delete_id = SqlConnect("kicp_faq").exec_sql(
                            'select faqId from faq_robot_extent where userId = 11 and robotId =877 and faqId not in ("101478400129073152","100717851615264768","100717550967554048","101305312947044352","101305407436324864","101305312947044352","101478344294498304")ORDER BY addTime DESC')[
                            0][0]
                        wb = openpyxl.load_workbook(rootPath + "testdata\\robotfaq\\faq_robot.xlsx")
                        sheet = wb["delete_faq"]
                        FaqDelete.modify(sheet, '正常删除', '{ "ids":"[' + str(delete_id) + ']"}')
                        FaqDelete.modify(sheet, '重复删除', '{ "ids":"[' + str(delete_id) + ']"}')
                        wb.save(rootPath + "testdata\\robotfaq\\faq_robot.xlsx")

                    except Exception as e:
                        print('修改表格出错！', '\n', e)

                    # 删除该测试账号下无用的账号,877为userId为11下的需要校验的robot manage，709用与查询robot config非空查询
                    SqlConnect("kicp_faq").delete_data(
                        'delete from faq_robot_extent where userId=11 and robotId=877 and faqId not in ("101478400129073152","100717851615264768","100717550967554048","101305312947044352","101305407436324864","101305312947044352","101478344294498304") and  faqId!=' + str(
                            delete_id))
                    print("删除成功")
                return re_code, except_data
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def modify(sheet, name, value):
        for index, row in enumerate(sheet.rows):
            if name == sheet['A' + str(index + 1)].value:
                sheet.cell(row=index + 1, column=2, value=value)

#
# if __name__ == '__main__':
#     actual_result, expect_result = FaqDelete().faq_delete(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"ids": ''}
#                    ),
#         'code-8')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
