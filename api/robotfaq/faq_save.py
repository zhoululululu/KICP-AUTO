# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_save.py
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


class FaqSave:

    @staticmethod
    def faq_save(url, params, assert_value):
        path = "/faqConfig/robotFAQ/save"
        try:
            value = eval(str(params)).get("data")
            if "code-8" in assert_value:
                question_data = eval(str(value)).get("question") + str(time.time())
                value = eval(str(value))
                value["question"] = question_data
            params = json.dumps({"data": json.dumps(value)})
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

# if __name__ == '__main__':
#     actual_result, expect_result = FaqSave().faq_save(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"data": json.dumps({"question": "ZL-测试配置问答对信息1", "categoryId": "895", "similarQuestionforms": [],
#                                         "answerForms": [{"content": "<div>ZL-测试配置问答对回答1</div>"}], "effectiveType": 0,
#                                         "sourceType": 0, "enable": "true", "userId": "11", "robotId": "877"})}
#                    ),
#         'code-8')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
