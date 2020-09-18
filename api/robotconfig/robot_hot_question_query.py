# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_hot_question_query.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
from commonfunc.get_db_connect import SqlConnect
from commonfunc.get_es_connect import ElasticConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotHotQuestionQuery:

    @staticmethod
    def hot_question_query(url, params, assert_value):
        path = "/robotConfig/robotCfg/config/hotQuestionQuery"
        try:
            result = requests.post(url=url + path, params=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data

            elif "sql" in assert_value and "bean" in result:
                re_result = json.dumps(result["bean"])
                expect_result = RobotHotQuestionQuery.get_hot_question_query(assert_value.split("-")[1])
                return re_result, expect_result
            elif "status" in assert_value:
                re_message = json.dumps(result["status"])
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_hot_question_query(sql):
        hot_question_list = []
        result = SqlConnect(
            "kicp_robot_config").exec_sql(sql)
        robot_id = str(result[0][0])
        hot_question_enable = True if result[0][1] == 1 else False
        hot_data_mode = result[0][2]
        guide_word = result[0][3]
        user_id = str(result[0][4])
        # if hot_question_enable == True:
        hot_question_result = SqlConnect(
            "kicp_robot_config").exec_sql(
            "select hql.recordId,hql.robotId,hql.faqId,hql.indexNo,hql.hotDataMode from robot_hot_question_list hql where hql.robotId ={} and hql.userId = {}".format(
                robot_id, user_id))
        for i in range(len(hot_question_result)):
            es_query_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "id": hot_question_result[i][2]
                                }
                            }
                        ]
                    }
                },
                "_source": "question"
            }
            question = ElasticConnect("robot_faq").get_search(es_query_body)["hits"]["hits"][0]["_source"][
                "question"]
            hot_question_list.append(
                {"recordId": str(hot_question_result[i][0]), "robotId": str(hot_question_result[i][1]),
                 "faqId": str(hot_question_result[i][2]),
                 "indexNo": str(hot_question_result[i][3]),
                 "hotDataMode": hot_question_result[i][4],
                 "question": question})

        query_result = {
            "robotId": robot_id, "hotQuestionEnable": hot_question_enable, "hotDataMode": hot_data_mode,
            "guideWord": guide_word,
            "hotQuestionList": hot_question_list, "userId": user_id,
        }

        return json.dumps(query_result)

# if __name__ == '__main__':
#     actual_result, expect_result = RobotHotQuestionQuery().hot_question_query("https://tkf-kicp.kuaishang.cn",
#                                                                               json.dumps(
#                                                                                   {"robotId": "877", "userId": "11"}),
#                                                                               "sql-select hq.robotId,hq.hotQuestionEnable,hq.hotDataMode,hq.guideWord,hq.userId from robot_hot_question hq where hq.robotId =877 and hq.userId = 11")
#     print(actual_result)
#     print(expect_result)
