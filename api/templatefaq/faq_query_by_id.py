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
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect

from requests_toolbelt import MultipartEncoder
import time
import math

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryById:

    @staticmethod
    def query_by_id(url, params, assert_value):
        path = "/faqConfig/robotFAQ/queryById"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "es" in assert_value:
                if "bean" in result:
                    re_message = result["bean"]
                else:
                    re_message = result
                expect_data = FaqQueryById.get_es_result(assert_value.split("--")[1], assert_value.split("--")[2])
                return json.dumps(re_message), json.dumps(expect_data)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_query_ids(question_ids):
        es_query_questions = {
            "query": {
                "ids":
                    {
                        "values": eval(question_ids)
                    }
            },
            "sort": [
                {
                    "modifyTime": {
                        "order": "desc"
                    }
                }
            ]

        }
        return es_query_questions

    def get_relatinship_id(id):
        relationship_id = {"query": {"match": {"id": id}}}
        return relationship_id

    def get_question_info(question_ids):
        question_result = []
        questions = ElasticConnect("robot_faq").get_search(
            FaqQueryById.get_query_ids(question_ids))["hits"]["hits"]
        for i in range(len(questions)):
            question_single = {
                "id": str(questions[i]["_source"].get("id")),
                "question": questions[i]["_source"].get("question"),
                "parentId": str(questions[i]["_source"].get("parentId")),
                "categoryId": str(questions[i]["_source"].get("categoryId")),
                "enable": questions[i]["_source"].get("enable"),
                "effectiveType": questions[i]["_source"].get("effectiveType"),
                "addTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(float(questions[i]["_source"].get("addTime")) / 1000)),
                "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime(float(questions[i]["_source"].get("modifyTime")) / 1000)),
                "userId": str(questions[i]["_source"].get("userId")),
                "robotId": str(questions[i]["_source"].get("robotId"))
            }
            question_result.append(question_single)
        return question_result

    def get_answer_info(question_ids):
        answer_result = []
        answers = ElasticConnect("robot_faq_answer").get_search(
            FaqQueryById.get_query_ids(question_ids))["hits"]["hits"]
        for i in range(len(answers)):
            answer_single = {
                "id": str(answers[i]["_source"].get("id")),
                "condition": answers[i]["_source"].get("condition"),
                "parentFAQId": str(answers[i]["_source"].get("parentFAQId")),
                "categoryId": str(answers[i]["_source"].get("categoryId")),
                "content": answers[i]["_source"].get("content"),
                "addTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(float(answers[i]["_source"].get("addTime")) / 1000)),
                "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime(float(answers[i]["_source"].get("modifyTime")) / 1000)),
                "userId": str(answers[i]["_source"].get("userId")),
                "robotId": str(answers[i]["_source"].get("robotId"))
            }
            if answers[i]["_source"].get("condition") == None:
                answer_single.pop("condition")
            answer_result.append(answer_single)
        return answer_result

    def get_es_result(index, es_query):
        es_result = []
        result = ElasticConnect(index).get_search(es_query)
        question_info = result["hits"]["hits"][0].get("_source")
        similar_questions, related_questions, related_questions = [], [], []
        if question_info.get("similarQuestionIds") is not None:
            similar_questions = FaqQueryById.get_question_info(question_info.get("similarQuestionIds"))
        if question_info.get("relateQuestionIds") is not None:
            for i in eval(question_info.get("relateQuestionIds")):
                related_question = FaqQueryById.get_es_result("robot_faq", FaqQueryById.get_relatinship_id(i))
                related_questions.append(related_question)
        if question_info.get("answerIds") is not None:
            answers = FaqQueryById.get_answer_info(question_info.get("answerIds"))
        es_result = {
            "id": str(question_info.get("id")),
            "question": question_info.get("question"),
            "parentId": str(question_info.get("parentId")),
            "similarQuestionIds": question_info.get("similarQuestionIds"),
            "similarQuestionforms": similar_questions,
            "categoryId": str(question_info.get("categoryId")),
            "hits": str(question_info.get("hits")),
            "enable": question_info.get("enable"),
            "effectiveType": question_info.get("effectiveType"),
            "relateQuestionIds": question_info.get("relateQuestionIds"),
            "relateQuestionForms": related_questions,
            "answerIds": question_info.get("answerIds"),
            "answerForms": answers,
            "addTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(float(question_info.get("addTime")) / 1000)),
            "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime(float(question_info.get("modifyTime")) / 1000)),
            "userId": str(question_info.get("userId")),
            "robotId": str(question_info.get("robotId")),
            "sourceType": str(question_info.get("sourceType"))
        }
        if question_info.get("relateQuestionIds") is None:
            es_result.pop("relateQuestionIds")
        if question_info.get("similarQuestionIds") is None:
            es_result.pop("similarQuestionIds")
        return es_result
        #


# if __name__ == '__main__':
#     actual_result, expect_result = FaqQueryById().query_by_id(
#         "https://tkf-kicp.kuaishang.cn",
#         json.dumps({"id": "101305312947044352"}
#                    ),
#         'es--robot_faq--{"query":{"match":{"id":"101305312947044352"}}}')
#     print(actual_result)
#     print(expect_result)
#     assert Assert.get_result(actual_result, expect_result)
