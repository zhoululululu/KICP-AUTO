# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query_category.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
import time
from commonfunc.get_es_connect import ElasticConnect
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryCategory:

    @staticmethod
    def faq_query_category(url, params, assert_value):
        path = "/faqConfig/fAQRobotCategory/search"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "sql" in assert_value:
                re_bean = len(result["bean"])
                sql_result = FaqQueryCategory.get_expect_result(assert_value.split("-")[1],
                                                                assert_value.split("-")[2])
                return str(re_bean), str(sql_result)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_expect_result(index, sql):
        final_result = []
        sql_result = len(SqlConnect(
            index).exec_sql(sql))+1
        return sql_result


#
if __name__ == '__main__':
    actual_result, expect_result = FaqQueryCategory().faq_query_category(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"userId": "11", "robotId": "877", "keyName": "question", "keyword": "zl"}
                   ),
        'sql-kicp_faq-select categoryId from faq_robot_category where userId = 11 and robotId = 877;')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
