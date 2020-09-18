# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.assert_func import Assert
from commonfunc.get_es_connect import ElasticConnect
import time
import math

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQuery:

    @staticmethod
    def faq_query(url, params, assert_value):
        path = "/faqConfig/robotFAQ/queryPage"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "es" in assert_value:
                re_result = result["bean"]
                except_data = FaqQuery.get_expect_result(params, assert_value.split("-")[1], assert_value.split("-")[2])
                return json.dumps(re_result), json.dumps(except_data)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_expect_result(params, index, es_query):

        get_question = ElasticConnect(index).get_search(es_query)["hits"]
        es_results, final_result = [], {}
        for i in range(len(get_question["hits"])):
            result = {
                "id": str(get_question["hits"][i]["_source"].get("id")),
                "question": get_question["hits"][i]["_source"].get("question"),
                "parentId": str(get_question["hits"][i]["_source"].get("parentId")),
                "similarQuestionIds": get_question["hits"][i]["_source"].get("similarQuestionIds"),
                "categoryId": str(get_question["hits"][i]["_source"].get("categoryId")),
                "hits": str(get_question["hits"][i]["_source"].get("hits")),
                "enable": get_question["hits"][i]["_source"].get("enable"),
                "effectiveType": get_question["hits"][i]["_source"].get("effectiveType"),
                "relateQuestionIds": get_question["hits"][i]["_source"].get("relateQuestionIds"),
                "answerIds": get_question["hits"][i]["_source"].get("answerIds"),
                "addTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(
                                             float(get_question["hits"][i]["_source"].get("addTime")) / 1000)),
                "modifyTime": time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.localtime(
                                                float(get_question["hits"][i]["_source"].get("modifyTime")) / 1000)),
                "userId": str(get_question["hits"][i]["_source"].get("userId")),
                "robotId": str(get_question["hits"][i]["_source"].get("robotId")),
                "sourceType": str(get_question["hits"][i]["_source"].get("sourceType"))
            }
            if get_question["hits"][i]["_source"].get("relateQuestionIds") is None:
                result.pop("relateQuestionIds")
            if get_question["hits"][i][
                "_source"].get("similarQuestionIds") is None:
                result.pop("similarQuestionIds")
            if get_question["hits"][i]["_source"].get("enable") is None:
                result.pop("enable")
            if get_question["hits"][i]["_source"].get("categoryId") is None:
                result.pop("categoryId")
            es_results.append(result)
        final_result = {"resultlist": es_results,
                        "totalrecord": get_question["total"].get("value"),
                        "curPage": int(eval(params).get("curPage")) if "curPage" in params else 1,
                        "pageSize": int(eval(params).get("pageSize")) if "pageSize" in params else 10,
                        "totalPage": math.ceil(int(get_question["total"].get("value")) / (
                            int(eval(params).get("pageSize")) if "pageSize" in params else 10)),
                        "beginIndex": (int((eval(params).get("curPage")) if "curPage" in params else 1) - 1) * (
                            int(eval(
                                params).get(
                                "pageSize")) if "pageSize" in params else 10)}
        return final_result


#
if __name__ == '__main__':
    actual_result, expect_result = FaqQuery().faq_query(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"userId": "11","robotId": "877"}
                   ),
        'es-robot_faq-{"query":{"bool":{"must":[{"match":{"userId":11}},{"match":{"robotId":877}},{"match":{"parentId":0}}]}},"sort":[{"modifyTime":{"order":"desc"}}],"size":200}')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
