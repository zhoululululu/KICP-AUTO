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
                re_result = result["bean"]
                expect_result = FaqQueryTemplateStandardQuestion.get_es_result(assert_value, params,
                                                                               assert_value.split("--")[1],
                                                                               assert_value.split("--")[2])
                return json.dumps(re_result), json.dumps(expect_result)
            elif "esanswer" in assert_value and "bean" in result:
                if "font" in str(result["bean"]):
                    re_result = str(result["bean"]).replace("<font color='red'>", "").replace("</font>", "")
                else:
                    re_result = str(result["bean"])
                expect_result = FaqQueryTemplateStandardQuestion.get_es_result(assert_value, params,
                                                                                       assert_value.split("--")[1],
                                                                                       assert_value.split("--")[2])
                return json.dumps(eval(re_result)), json.dumps(expect_result)
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
            for i in range(len(result["hits"]["hits"])):
                faq_answer = ElasticConnect("template_faq_answer").get_search(
                    FaqQueryTemplateStandardQuestion.get_answer_result(
                        eval(result["hits"]["hits"][i]["_source"].get("answerIds"))))[
                    "hits"]["hits"][0]["_source"].get("content")
                first_result = result["hits"]["hits"][i].get("_source")
                final_result = {"id": str(first_result.get("id")),
                                'question': first_result.get("question"),
                                'answer': faq_answer,
                                'templateId': str(first_result.get("templateId")),
                                'modifyTime': time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime(
                                                                float(first_result.get("modifyTime")) / 1000)),
                                }
                resultlist.append(final_result)
                answer_list = []
            re_es_result = {'resultlist': resultlist,
                            'totalrecord': result["hits"]["total"].get("value"),
                            'curPage': eval(params).get("curPage") if "curPage" in params else 1,
                            'pageSize': eval(params).get("pageSize") if "pageSize" in params else 10,
                            'totalPage': math.ceil(int(result["hits"]["total"].get("value")) / (
                                eval(params).get("pageSize"))) if "pageSize" in params else 10,
                            'beginIndex': ((eval(params).get("curPage") if "curPage" in params else 1) - 1) * eval(
                                params).get(
                                "pageSize") if "pageSize" in params else 10}
            return re_es_result
        elif "answer" in assert_value:
            result = ElasticConnect(index_name).get_search(es_query)
            for i in range(len(result["hits"]["hits"])):
                faq_question = ElasticConnect("template_faq").get_search(
                    FaqQueryTemplateStandardQuestion.get_question_result(
                        str(result["hits"]["hits"][i]["_source"].get("parentFAQId"))))[
                    "hits"]["hits"][0]["_source"].get("question")
                first_result = result["hits"]["hits"][i].get("_source")
                final_result = {"id": str(first_result.get("id")),
                                'answer': first_result.get("content"),
                                'belongStandardQuestionId': str(first_result.get("parentFAQId")),
                                'belongStandardQuestion': faq_question,
                                'templateId': str(first_result.get("templateId")),
                                'modifyTime': time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime(
                                                                float(first_result.get("modifyTime")) / 1000))}
                resultlist.append(final_result)
                answer_list = []
            re_es_result = {'resultlist': resultlist,
                            'totalrecord': result["hits"]["total"].get("value"),
                            'curPage': eval(params).get("curPage") if "curPage" in params else 1,
                            'pageSize': eval(params).get("pageSize") if "pageSize" in params else 10,
                            'totalPage': math.ceil(int(result["hits"]["total"].get("value")) / (
                                eval(params).get("pageSize"))) if "pageSize" in params else 10,
                            'beginIndex': ((eval(params).get("curPage") if "curPage" in params else 1) - 1) * eval(
                                params).get(
                                "pageSize") if "pageSize" in params else 10}
            return re_es_result

    def get_question_result(question_id):
        query_question = {
            "query": {
                "match": {
                    "_id": str(question_id)
                }
            }, "_source": "question"
        }

        return query_question

    def get_answer_result(answer_id):
        query_answer = {
            "query": {
                "ids": {
                    "values": answer_id
                }
            },
            "_source": ["content"]
        }
        return query_answer


if __name__ == '__main__':
    actual_result, expect_result = FaqQueryTemplateStandardQuestion().query_template_standard_question(
        "https://tkf-kicp.kuaishang.cn", json.dumps(
            {"templateId": "5", "keyword": "瘦脸针要打几针", "keyName": "question", "curPage": 1, "pageSize": 10}),
        'esanswer--template_faq--{"query":{"bool":{"must":[{"match":{"templateId":5}},{"match":{"question":"瘦脸针要打几针"}}]}},"size":10,"from":0,"sort":[{"_score":{"order":"desc"}}]}')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
