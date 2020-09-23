# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_save_template.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect
import time
from requests_toolbelt import MultipartEncoder

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqSaveTemplate:

    @staticmethod
    def save_template_faq(url, params, assert_value):
        path = "/faqConfig/robotFAQ/save"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            if "code-8" in assert_value:
                value = eval(str(params)).get("data")
                question_data = eval(str(value)).get("question") + str(time.time())
                value = eval(str(value))
                value["question"] = question_data
            params = json.dumps({"data": json.dumps(value)})
            result = requests.post(url=url + path, data=json.loads(params), headers=header).json()
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
    actual_result, expect_result = FaqSaveTemplate().save_template_faq(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"data": {"question": "zl-test分类测试问题2", "categoryId": "904",
                             "similarQuestionforms": [{"question": "zl-test分类测试问题2-1"}], "answerForms": [
                {"content": "<div>zl-test分类测试回答2</div>",
                 "condition": "[{\"action\":\"include\",\"type\":\"input\",\"content\":\"分类测试\"}]"}],
                             "effectiveType": 0, "sourceType": 0, "enable": "true", "userId": "11", "robotId": "877"}}
                   ),
        'code-8')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
