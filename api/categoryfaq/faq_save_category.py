# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_save_category.py
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
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqSaveCategory:

    @staticmethod
    def faq_save_category(url, params, assert_value):
        path = "/faqConfig/fAQRobotCategory/save"
        try:
            if ("categoryName" in params and "1253" not in assert_value) or "code-8" in assert_value:
                new_params = eval(str(params))
                value = eval(str(params)).get("categoryName")
                new_params["categoryName"] = value + str(time.time())
                params = json.dumps(new_params)
            result = requests.post(url=url + path, data=json.loads(params)).json()
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
if __name__ == '__main__':
    actual_result, expect_result = FaqSaveCategory().faq_save_category(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"robotId": "877", "userId": "11", "categoryName": "ZL测试分类1"}),
        'code-1253')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
