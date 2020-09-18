# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_check_question.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqCheckQuestion:

    @staticmethod
    def faq_check_question(url, params, assert_value):
        path = "/faqConfig/fAQTemplate/checkQuestion"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                expect_result = assert_value.split("-")[1]
                return re_code, expect_result
            if "bean" in assert_value:
                if "bean" in result:
                    re_bean = str(result["bean"])
                else:
                    re_bean = result
                expect_result = assert_value.split("-")[1]
                return re_bean, expect_result
            elif "message" in assert_value:
                re_message = result["message"]
                expect_result = assert_value.split("-")[1]
                return re_message, expect_result
            else:
                return result, assert_value
        except Exception:
            raise Exception


#
if __name__ == '__main__':
    actual_result, expect_result = FaqCheckQuestion().faq_check_question(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"robotId": "877", "userId": "11", "question": "111", "size": "1"})
        ,
        'code-8')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
