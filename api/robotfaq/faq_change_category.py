# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_change_category.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqChangeCategory:

    @staticmethod
    def faq_change_category(url, params, assert_value):
        path = "/faqConfig/robotFAQ/changeCategory"
        try:
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
# if __name__ == '__main__':
#     actual_result, expect_result = FaqChangeCategory().faq_change_category(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({
#                        "ids": '["100713822935941120","100718255342190592","100717851615264768","100717550967554048","100515541475753984"]',
#                        "category": "904"}
#                    ),
#         'code-8')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
