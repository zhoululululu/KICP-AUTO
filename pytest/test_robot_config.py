# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 14:16
@File  : test_robot_config.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.robotconfig.robot_threshold_query import RobotThresholdQuery
from api.robotconfig.robot_threshold_save import RobotThresholdSave
from api.robotconfig.robot_greeting_query import RobotGreetingQuery
from api.robotconfig.robot_warm_word_query import RobotWarmWordQuery
from api.robotconfig.robot_un_problem_query import RobotUnProblemQuery
from api.robotconfig.robot_guide_query import RobotGuideQuery
from commonfunc.change_data_type import ChangeDataType
from commonfunc.assert_func import Assert
import os
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class TestRobotConfig:
    threshold_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                        sheet_name="query_threshold_data")
    threshold_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                       sheet_name="save_threshold_data")
    greeting_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                       sheet_name="query_greeting")
    guide_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                    sheet_name="query_guide")
    warm_word_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                        sheet_name="query_warm_word")
    un_problem_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                         sheet_name="query_unproblem")

    def setup_class(self):
        self.url = "https://tkf-kicp.kuaishang.cn"

    @pytest.mark.parametrize('desc,params,assert_value', threshold_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人阈值范围查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_threshold_query(self, desc, params, assert_value):
        """
        机器人阈值范围查询
        """
        actual_result, except_result = RobotThresholdQuery.threshold_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', threshold_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人阈值范围保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_threshold_save(self, desc, params, assert_value):
        """
        机器人阈值范围保存
        """
        actual_result, except_result = RobotThresholdSave.threshold_save(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', greeting_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人问候语查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_greeting_query(self, desc, params, assert_value):
        """
        机器人问候语查询
        """
        actual_result, except_result = RobotGreetingQuery.greeting_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', guide_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人引导语查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_guide_query(self, desc, params, assert_value):
        """
        机器人引导语查询
        """
        actual_result, except_result = RobotGuideQuery.guide_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', warm_word_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人暖场语查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_warm_word_query(self, desc, params, assert_value):
        """
        机器人暖场语查询
        """
        actual_result, except_result = RobotWarmWordQuery.warm_word_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', un_problem_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人未知问题回复查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_un_problem_query(self, desc, params, assert_value):
        """
        机器人未知问题回复查询
        """
        actual_result, except_result = RobotUnProblemQuery.un_problem_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)
