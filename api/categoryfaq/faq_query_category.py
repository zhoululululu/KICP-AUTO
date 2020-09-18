# -*- coding: UTF-8 -*-
'''
Created on 2020/9/15 9:38
@File  : faq_query_category.py
@author: ZL
@Desc  :
'''
import requests
import json
import os
import time
from commonfunc.get_es_connect import ElasticConnect
from commonfunc.assert_func import Assert
from commonfunc.get_db_connect import SqlConnect

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class FaqQueryCategory:

    @staticmethod
    def faq_query_category(url, params, assert_value):
        path = "/faqConfig/fAQRobotCategory/search"
        try:
            result = requests.post(url=url + path, data=json.loads(params)).json()
            if "code" in assert_value:
                re_code = str(result["code"])
                except_data = assert_value.split("-")[1]
                return re_code, except_data
            elif "sql" in assert_value:
                re_bean = result["bean"]
                sql_result = FaqQueryCategory.get_final_result(params, assert_value.split("-")[1],
                                                               assert_value.split("-")[2])
                return json.dumps(re_bean), json.dumps(sql_result)
            elif "message" in assert_value:
                re_message = result["message"]
                expect_data = assert_value.split("-")[1]
                return re_message, expect_data
            else:
                return result, assert_value
        except Exception:
            raise Exception

    def get_es_query(category_id, user_id, robot_id):
        es_query_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {
                            "categoryId": int(category_id)
                        }},
                        {"match": {
                            "userId": int(user_id)
                        }},
                        {"match": {
                            "robotId": int(robot_id)
                        }},
                        {"match": {
                            "parentId": "0"
                        }}
                    ]
                }
            }
        }
        return es_query_body

    def get_sql_query(category_id):
        faq_robot_category_forms = "select categoryId,categoryName,parentId,indexNo,robotId,addTime,modifyTime,userId,isunAllot from faq_robot_category where userId = 11 and robotId = 877 and parentId={} order by modifyTime".format(
            category_id)
        return faq_robot_category_forms

    def get_expect_result(index, sql):
        final_result = []
        sql_result = SqlConnect(
            index).exec_sql(sql)
        if len(sql_result) != 0:
            for i in range(len(sql_result)):
                category_id = sql_result[i][0]
                es_result = ElasticConnect("robot_faq").get_search(
                    FaqQueryCategory.get_es_query(str(category_id), str(sql_result[i][7]), str(sql_result[i][4])))[
                    "hits"]["total"].get("value")
                result_single = {
                    "categoryId": str(sql_result[i][0]),
                    "categoryName": sql_result[i][1],
                    "parentId": str(sql_result[i][2]),
                    "indexNo": str(sql_result[i][3]),
                    "robotId": str(sql_result[i][4]),
                    "addTime": str(sql_result[i][5]),
                    "modifyTime": str(sql_result[i][6]),
                    "userId": str(sql_result[i][7]),
                    "questionNum": es_result,
                    "faqRobotCategoryForms": FaqQueryCategory.get_expect_result("kicp_faq",
                                                                                FaqQueryCategory.get_sql_query(
                                                                                    category_id)),
                    "unAllot": True if sql_result[i][8] == 1 else False}
                if result_single.get("categoryName") == "未分类":
                    result_single.pop("faqRobotCategoryForms")
                final_result.append(result_single)
        return final_result

    def get_final_result(params, index, sql):
        userId = eval(params).get("userId")
        robotId = eval(params).get("robotId")
        result = FaqQueryCategory.get_expect_result(index, sql)
        questionNum = ElasticConnect("robot_faq").get_search(
            FaqQueryCategory.get_es_query("0", userId, robotId))["hits"]["total"].get("value")
        unpack = {
            "categoryId": "0",
            "categoryName": "未分类",
            "questionNum": questionNum,
            "unAllot": True
        }
        result.append(unpack)
        return result
        # #

#
if __name__ == '__main__':
    actual_result, expect_result = FaqQueryCategory().faq_query_category(
        "https://tkf-kicp.kuaishang.cn",
        json.dumps({"userId": "11", "robotId": "877"}
                   ),
        'sql-kicp_faq-select categoryId,categoryName,parentId,indexNo,robotId,addTime,modifyTime,userId,isunAllot from faq_robot_category where userId = 11 and robotId = 877 and categoryName!="未分类" order by indexNo desc')
    print(actual_result)
    print(expect_result)
    assert Assert.get_result(actual_result, expect_result)
