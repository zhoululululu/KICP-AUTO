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
from commonfunc.get_es_connect import ElasticConnect
from commonfunc.assert_func import Assert

from commonfunc.get_db_connect import SqlConnect
import openpyxl

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqDelete:

    @staticmethod
    def faq_delete(url, params, assert_value):
        path = "/faqConfig/robotFAQ/delete"
        delete_id_list = []
        not_delete_id = ["101478400129073152", "101305312947044352",
                         "101305407436324864", "101478344294498304"]
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                if re_code == "8":
                    try:
                        # 针对delete额外操作：修改用例表,将faqId重新从库中寻找
                        delete_id = ElasticConnect("robot_faq").get_search(FaqDelete.query_es())["hits"]["hits"][0].get(
                            "_id")
                        not_delete_id.append(delete_id)
                        wb = openpyxl.load_workbook(rootPath + "testdata\\robotfaq\\faq_robot.xlsx")
                        sheet = wb["delete_faq"]
                        FaqDelete.modify(sheet, '正常删除', '{ "ids":"[' + str(delete_id) + ']"}')
                        FaqDelete.modify(sheet, '重复删除', '{ "ids":"[' + str(delete_id) + ']"}')
                        wb.save(rootPath + "testdata\\robotfaq\\faq_robot.xlsx")

                    except Exception as e:
                        print('修改表格出错！', '\n', e)

                    # 删除该测试账号下无用的账号,877为userId为11下的需要校验的robot manage，709用与查询robot config非空查询
                    es_result = ElasticConnect("robot_faq").get_search(FaqDelete.query_es())["hits"]["hits"]
                    for i in es_result:
                        if i.get("_id") not in not_delete_id:
                            delete_id_list.append(int(i.get("_id")))
                    new_delete = json.dumps(eval('{ "ids":"' + str(delete_id_list) + '"}'))
                    aother_result = requests.post(url=url + path,
                                                  data=json.loads(new_delete)).json()
                    print("删除多余faq成功")
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

    @staticmethod
    def query_es():
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "parentId": 0
                            }
                        },
                        {
                            "match": {
                                "robotId": 877
                            }
                        }]
                }
            },
            "_source": ["id", "parentId"],
            "size": 200,
            "sort": [
                {
                    "addTime": {
                        "order": "desc"
                    }
                }
            ]
        }
        return query


if __name__ == '__main__':
    actual_result, expect_result = FaqDelete().faq_delete(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({
            "ids": '[101555799734714368, 101555584986349576, 101547093836005378, 102966120965832706, 103047622265241600, 103052411153776640, 102966120965832704, 103056280919310336, 102701022699421696, 103056280919310338, 103056426948198402, 103056426948198400, 103339753055813632, 103344434570166278, 103342257021747206, 103340959941623808, 103343940648927232, 101547093836005382, 101538499606446082, 101555584986349573, 101555584986349570, 101555584986349568, 101554902086549506, 103056280919310342]'}
        ),
        'code-8')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
