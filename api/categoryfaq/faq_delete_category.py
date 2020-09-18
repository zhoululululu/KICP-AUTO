# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_delte_category.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect

from requests_toolbelt import MultipartEncoder
from commonfunc.get_db_connect import SqlConnect
import openpyxl

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqDeleteCategory:

    @staticmethod
    def delete_category_faq(url, params, assert_value):
        path = "/faqConfig/fAQRobotCategory/delete"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                if re_code == "8":
                    try:
                        # 针对delete额外操作：修改用例表,将faqId重新从库中寻找
                        delete_id = SqlConnect("kicp_faq").exec_sql(
                            'select categoryId from faq_robot_category where userId = 11 and robotId =877  and categoryId not in ("904","916","895")  ORDER BY addTime DESC')[
                            0][0]
                        wb = openpyxl.load_workbook(rootPath + "testdata\\robotfaq\\faq_robot_category.xlsx")
                        sheet = wb["delete_category"]
                        FaqDeleteCategory.modify(sheet, '正常删除', '{ "id":' + str(delete_id) + '}')
                        FaqDeleteCategory.modify(sheet, '重复删除', '{ "id":' + str(delete_id) + '}')
                        wb.save(rootPath + "testdata\\robotfaq\\faq_robot_category.xlsx")

                    except Exception as e:
                        print('修改表格出错！', '\n', e)

                    # 删除该测试账号下无用的账号,358为userId为11下的需要校验的robot manage，709用与查询robot config非空查询
                    SqlConnect("kicp_faq").delete_data(
                        'delete from faq_robot_category where userId=11 and robotId=877 and categoryId not in ("904","916","895") and categoryId!=' + str(
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
if __name__ == '__main__':
    actual_result, expect_result = FaqDeleteCategory().delete_category_faq(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"id": "898"}
                   ),
        'code-8')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
