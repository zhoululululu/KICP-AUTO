# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query_template_page.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_es_connect import ElasticConnect
import math
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryTemplatePage:

    @staticmethod
    def query_template_page(url, params, assert_value):
        path = "/faqConfig/template/queryPage"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "bean" in assert_value:
                re_bean = json.dumps(result["bean"])
                except_data = json.dumps(eval(assert_value.split("-")[1]))
                return re_bean, except_data
            elif "es" in assert_value and "bean" in result:
                re_result = json.dumps(result["bean"])
                expect_result = FaqQueryTemplatePage.get_es_result(params, assert_value.split("--")[1],
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

    def get_answer_query(answer_id):
        query_answer = {
            "query": {
                "ids": {
                    "values": answer_id
                }
            },
            "_source": ["content", "parentFAQId", "categoryId", "addTime", "modifyTime", "templateId"]
        }
        return query_answer

    def get_es_result(params, index_name, es_query):
        es_result, answer_list, resultlist, final_result_list = [], [], [], []
        result = ElasticConnect(index_name).get_search(
            es_query)
        normal_result = result["hits"]
        for i in range(len(normal_result["hits"])):
            faq_answer = ElasticConnect("template_faq_answer").get_search(
                FaqQueryTemplatePage.get_answer_query(eval(normal_result["hits"][i]["_source"].get("answerIds"))))[
                "hits"]["hits"]
            for j in range(len(faq_answer)):
                faq_answer[j].get("_source")
                answer_list.append({
                    "content": faq_answer[j]["_source"].get("content"),
                    "parentFAQId": str(faq_answer[j]["_source"].get("parentFAQId")),
                    "categoryId": str(faq_answer[j]["_source"].get("categoryId")),
                    "addTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(float(faq_answer[j]["_source"].get("addTime")) / 1000)),
                    "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime(
                                                    float(faq_answer[j]["_source"].get("modifyTime")) / 1000)),
                    "templateId": str(faq_answer[j]["_source"].get("templateId"))
                })
            first_result = normal_result["hits"][i].get("_source")
            final_result = {"id": str(first_result.get("id")),
                            'question': first_result.get("question"),
                            'categoryId': str(first_result.get("categoryId")),
                            'answerIds': first_result.get("answerIds"),
                            'addTime': time.strftime("%Y-%m-%d %H:%M:%S",
                                                     time.localtime(float(first_result.get("addTime")) / 1000)),
                            'modifyTime': time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.localtime(float(first_result.get("modifyTime")) / 1000)),
                            'templateId': str(first_result.get("templateId")),
                            'answerForms': answer_list,
                            }
            resultlist.append(final_result)
            answer_list = []
        es_result = {
            "resultlist": resultlist,
            "totalrecord": normal_result["total"].get("value"),
            "curPage": eval(params).get("curPage") if "curPage" in params else 1,
            "pageSize": eval(params).get("pageSize") if "pageSize" in params else 10,
            "totalPage": math.ceil(int(normal_result["total"].get("value")) / (
                eval(params).get("pageSize"))) if "pageSize" in params else 10,
            "beginIndex": ((eval(params).get("curPage") if "curPage" in params else 1) - 1) * eval(params).get(
                "pageSize") if "pageSize" in params else 10
        }
        return json.dumps(es_result)


# #
# if __name__ == '__main__':
#     actual_result, expect_result = FaqQueryTemplatePage().query_template_page(
#         "https://tkf-kicp.kuaishang.cn", json.dumps(
#             {"templateId": "5", "curPage": 1, "pageSize": 10, "keyword": "瘦脸针", "keyName": "question",
#              "orderName": "modifyTime", "orderBy": "desc"}),
#         'es--template_faq--{"query":{"bool":{"must":[{"match":{"categoryId":0}},{"match":{"templateId":5}},{"match":{"question":"瘦脸针"}}]}},"size":10,"from":0,"sort":[{"modifyTime":{"order":"desc"}}]}')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
