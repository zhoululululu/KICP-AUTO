# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_search_page.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
import math
import time
from commonfunc.get_es_connect import ElasticConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqSearchPage:

    @staticmethod
    def faq_search_page(url, params, assert_value):
        path = "/faqConfig/robotFAQ/searchPage"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "es" in assert_value:
                re_result = eval(str(result["bean"]).replace('<font color=\'red\'>', "").
                                 replace('</font>', "")) if '<font color=\'red\'>' in str(result["bean"]) else result[
                    "bean"]
                except_data = FaqSearchPage.get_expect_result(params, assert_value.split("-")[1],
                                                              assert_value.split("-")[2])
                return json.dumps(re_result), json.dumps(except_data)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_question_query(question_id):
        question_query = {
            "query": {
                "match": {
                    "id": str(question_id)
                }
            }
        }
        return question_query

    def get_expect_result(params, index, es_query):

        get_es_result = ElasticConnect(index).get_search(es_query)["hits"]
        es_results, final_result = [], {}
        for i in range(len(get_es_result["hits"])):
            if "question" in params:
                result = {
                    "id": str(get_es_result["hits"][i]["_source"].get("id")),
                    "question": get_es_result["hits"][i]["_source"].get("question"),
                    "similarQuestionCount": len(eval(get_es_result["hits"][i]["_source"].get("similarQuestionIds"))) if
                    get_es_result["hits"][i]["_source"].get("similarQuestionIds") is not None else 0,
                    "effectiveType": get_es_result["hits"][i]["_source"].get("effectiveType"),
                    "userId": str(get_es_result["hits"][i]["_source"].get("userId")),
                    "robotId": str(get_es_result["hits"][i]["_source"].get("robotId")),
                    "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime(
                                                    float(
                                                        get_es_result["hits"][i]["_source"].get("modifyTime")) / 1000))
                }
                if "keyword" not in params and get_es_result["hits"][i]["_source"].get("similarQuestionIds") is None:
                    result.pop("similarQuestionCount")

            elif "similarQuestion" in params:
                belongStandardQuestion = ElasticConnect("robot_faq").get_search(
                    FaqSearchPage.get_question_query(str(get_es_result["hits"][i]["_source"].get("parentId"))))["hits"][
                    "hits"][0]["_source"].get("question")
                result = {
                    "id": str(get_es_result["hits"][i]["_source"].get("id")),
                    "similarQuestion": get_es_result["hits"][i]["_source"].get("question"),
                    "belongStandardQuestionId": str(get_es_result["hits"][i]["_source"].get("parentId")),
                    "belongStandardQuestion": belongStandardQuestion,
                    "effectiveType": get_es_result["hits"][i]["_source"].get("effectiveType"),
                    "effectiveStartTime": str(get_es_result["hits"][i]["_source"].get("effectiveStartTime")),
                    "effectiveEndTime": str(get_es_result["hits"][i]["_source"].get("effectiveEndTime")),
                    "userId": str(get_es_result["hits"][i]["_source"].get("userId")),
                    "robotId": str(get_es_result["hits"][i]["_source"].get("robotId")),
                }
            elif "answer" in params:
                question_result = ElasticConnect("robot_faq").get_search(
                    FaqSearchPage.get_question_query(str(get_es_result["hits"][i]["_source"].get("parentFAQId"))))[
                    "hits"][
                    "hits"][0]["_source"]
                belongStandardQuestion = question_result.get("question")
                effectiveType = question_result.get("effectiveType")
                effectiveStartTime = str(question_result.get("effectiveStartTime"))
                effectiveEndTime = str(question_result.get("effectiveEndTime"))
                result = {
                    "id": str(get_es_result["hits"][i]["_source"].get("id")),
                    "answer": get_es_result["hits"][i]["_source"].get("content"),
                    "belongStandardQuestionId": str(get_es_result["hits"][i]["_source"].get("parentFAQId")),
                    "belongStandardQuestion": belongStandardQuestion,
                    "effectiveType": effectiveType,
                    "effectiveStartTime": effectiveStartTime,
                    "effectiveEndTime": effectiveEndTime,
                    "userId": str(get_es_result["hits"][i]["_source"].get("userId")),
                    "robotId": str(get_es_result["hits"][i]["_source"].get("robotId")),
                }
            es_results.append(result)
        final_result = {"resultlist": es_results,
                        "totalrecord": get_es_result["total"].get("value"),
                        "curPage": int(eval(params).get("curPage")) if "curPage" in params else 1,
                        "pageSize": int(eval(params).get("pageSize")) if "pageSize" in params else 10,
                        "totalPage": math.ceil(int(get_es_result["total"].get("value")) / (
                            int(eval(params).get("pageSize")) if "pageSize" in params else 10)),
                        "beginIndex": (int((eval(params).get("curPage")) if "curPage" in params else 1) - 1) * (
                            int(eval(
                                params).get(
                                "pageSize")) if "pageSize" in params else 10)}
        return final_result

# if __name__ == '__main__':
#     actual_result, expect_result = FaqSearchPage().faq_search_page(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"userId": "11","robotId": "877","keyName": "question","keyword": "分类","curPage": "1","pageSize": "10"}
#                    ),
#         'es-robot_faq-{"query":{"bool":{"must":[{"match":{"userId":11}},{"match":{"robotId":877}},{"match":{"parentId":0}},{"match":{"question":"分类"}}]}},"sort":[{"_score":{"order":"desc"}}]}')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
