# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query_template_standard_question.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
import time
import math
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryTemplateStandardQuestion:

    @staticmethod
    def query_template_standard_question(url, params, assert_value):
        path = "/faqConfig/template/searchStandardQuestions"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "esquestion" in assert_value and "bean" in result:
                re_result = result["bean"]["totalrecord"]
                expect_result = FaqQueryTemplateStandardQuestion.get_es_result(assert_value, params,
                                                                               assert_value.split("--")[1],
                                                                               assert_value.split("--")[2])
                return str(re_result), str(expect_result)
            elif "esanswer" in assert_value and "bean" in result:
                re_result = result["bean"]["totalrecord"]
                expect_result = FaqQueryTemplateStandardQuestion.get_es_result(assert_value, params,
                                                                               assert_value.split("--")[1],
                                                                               assert_value.split("--")[2])
                return str(re_result), str(expect_result)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_es_result(assert_value, params, index_name, es_query):
        answer_list, resultlist = [], []
        if "question" in assert_value:
            result = ElasticConnect(index_name).get_search(es_query)
            totle_num = result["hits"]["total"].get("value")
            return totle_num

        elif "answer" in assert_value:
            result = ElasticConnect(index_name).get_search(es_query)
            totle_num = result["hits"]["total"].get("value")
            return totle_num


if __name__ == '__main__':
    actual_result, expect_result = FaqQueryTemplateStandardQuestion().query_template_standard_question(
        "https://tkf-kicp.kuaishang.cn", json.dumps(
            {"templateId": "5", "keyword": "瘦脸针", "keyName": "answer", "curPage": 1, "pageSize": 10}),
        'esanswer--template_faq_answer--{"query":{"bool":{"must":[{"match":{"templateId":5}},{"match":{"content":"瘦脸针"}}]}},"size":10,"from":0,"sort":[{"_score":{"order":"desc"}}]}')
    assert Assert.get_result(actual_result, expect_result)
