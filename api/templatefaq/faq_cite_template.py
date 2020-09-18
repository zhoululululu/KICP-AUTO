# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_cite_template.py
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

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqCiteTemplate:

    @staticmethod
    def cite_template_faq(url, params, assert_value):
        path = "/faqConfig/fAQTemplate/citeToRobot"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
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
# if __name__ == '__main__':
#     actual_result, expect_result = FaqCiteTemplate().cite_template_faq(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"data": json.dumps(
#             {"id": "95648709596807168", "question": "   发热怎么办", "categoryId": 0, "answerIds": "[\"96813111782244352\"]",
#              "addTime": "2020-09-02 18:05:50", "modifyTime": "2020-09-05 21:24:19", "templateId": "5", "answerForms": [{
#                 "content": "您有发热，建议您测量一下体温，如果体温大于37度三，建议您到医院完善血常规，c反应蛋白等相关检查。建议您多喝点温开水，注意休息，做好自我防护，出门时一定要戴口罩，注意勤洗手，室内要通风换气，保持清新。",
#                 "parentFAQId": "95648709596807168",
#                 "categoryId": "0",
#                 "addTime": "2020-09-05 21:24:19",
#                 "modifyTime": "2020-09-05 21:24:19",
#                 "templateId": "5"}],
#              "key": "95648709596807168", "effectiveType": 0, "enable": True, "sourceType": 1, "userId": "11",
#              "robotId": "877"})}
#         ),
#         'code-8')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
