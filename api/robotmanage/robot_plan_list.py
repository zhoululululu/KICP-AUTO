# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 9:54
@File  : robot_plan_list.py
@author: ZL
@Desc  :
'''
import requests
from commonfunc.get_db_connect import SqlConnect
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class RobotPlanList:

    @staticmethod
    def plan_list(url):
        path = "/robotConfig/robotCfg/basic/planList"
        re_result_list, single_list = (), []
        try:
            result = requests.get(url=url + path).json()
            if "bean" in result:
                result_list = result["bean"]
                sql_result = SqlConnect(
                    "kicp_basic_data").exec_sql(
                    "select packageId,robotType,packageName,dataStatus from robot_package_list")
                for i in range(len(result_list)):
                    single_list.append(
                        (int(result_list[i]["packageId"]), result_list[i]["robotType"], result_list[i]["packageName"],
                         1 if result_list[i]["dataStatus"] == True else 0))
                return sorted(single_list), sorted(list(sql_result))
            else:
                return result, "请手动检查结果"
        except Exception:
            raise Exception


# if __name__ == '__main__':
    # select templateId,templateName,dataStatus from kicp_template.template
    # re_result_list, sql_result = RobotPlanList().plan_list("https://tkf-kicp.kuaishang.cn")
# assert len(re_result_list) == len(set(re_result_list) & set(sql_result))
