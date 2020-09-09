# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_template_list.py
@author: ZL
@Desc  :
'''
import requests
from commonfunc.get_db_connect import SqlConnect
import json
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotTemplateList:

    @staticmethod
    def template_list(url):
        path = "/template/template/templateList"
        re_result_list, single_list = (), []
        try:
            result = requests.get(url=url + path).json()
            if "bean" in result:
                result_list = result["bean"]
                sql_result = SqlConnect(
                    "kicp_template").exec_sql("select templateId,templateName,dataStatus from template")
                for i in range(len(result_list)):
                    single_list.append((int(result_list[i]["templateId"]), result_list[i]["templateName"],
                                        1 if result_list[i]["dataStatus"] == True else 0))
                return sorted(single_list), sorted(list(sql_result))
            else:
                return result
        except Exception:
            raise Exception

# if __name__ == '__main__':
# select templateId,templateName,dataStatus from kicp_template.template
# re_result_list, sql_result = RobotTemplateList().template_list("https://tkf-kicp.kuaishang.cn",
#                                                                "sql-select templateId,templateName,dataStatus from template")
# assert len(re_result_list) == len(set(re_result_list) & set(sql_result))
