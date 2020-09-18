# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query_template_category.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryTemplateCategory:

    @staticmethod
    def query_template_category(url, params, assert_value):
        path = "/faqConfig/fAQTemplateCategory/search"
        try:
            result = requests.post(url=url + path, params=json.loads(params.encode("UTF-8"))).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "es" in assert_value and "bean" in result:
                re_result = result["bean"]
                expect_result = FaqQueryTemplateCategory.get_es_result(assert_value.split("--")[1],
                                                                       assert_value.split("--")[2])
                return re_result, expect_result
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_es_result(index_name, es_query):
        es_result = []
        result = ElasticConnect(index_name).get_search(es_query)
        categorys = result["hits"]
        es_result.append({
            "categoryId": "0",
            "categoryName": "未分类",
            "questionNum": categorys["total"].get("value"),
            "unAllot": True
        })
        return es_result


#
# if __name__ == '__main__':
    # actual_result, expect_result = FaqQueryTemplateCategory().query_template_category(
    #     "https://tkf-kicp.kuaishang.cn", json.dumps(
    #         {"templateId": "5", "keyName": "answer", "keyword": "瘦脸针", "modifyTimeFrom": "2020-08-01 23:36:52",
    #          "modifyTimeTo": "2020-09-05 23:36:52"}),
    #     'es--template_faq_answer--{"query":{"bool":{"must":[{"match":{"categoryId":0}},{"match":{"templateId":5}},{"match":{"content":"瘦脸针"}},{"range":{"modifyTime":{"gt":"2020-08-01T23:36:52","lt":"2020-09-05T23:36:52"}}}]}}}')
    # print(actual_result)
    # print(expect_result)
    # assert Assert.get_result(actual_result, expect_result)
