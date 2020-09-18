# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 14:16
@File  : test_robot_faq.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.robotfaq.faq_check_question import FaqCheckQuestion
from api.robotfaq.faq_search_page import FaqSearchPage
from api.robotfaq.faq_change_category import FaqChangeCategory
from api.robotfaq.faq_change_status import FaqChangeStatus
from api.robotfaq.faq_delete import FaqDelete
from api.robotfaq.faq_query import FaqQuery
from api.robotfaq.faq_save import FaqSave
from commonfunc.change_data_type import ChangeDataType
from commonfunc.assert_func import Assert
import os
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class TestRobotFaq:
    query_faq = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                             sheet_name="query_faq")
    save_faq = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                            sheet_name="save_faq")
    delete_faq = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                              sheet_name="delete_faq")
    check_question = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                                  sheet_name="check_question")
    change_status = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                                 sheet_name="change_status")
    change_category = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                                   sheet_name="change_category")
    search_page = ChangeDataType.get_test_data("robotfaq\\faq_robot.xlsx",
                                               sheet_name="search_page")

    def setup_class(self):
        self.url = "https://tkf-kicp.kuaishang.cn"

    @pytest.mark.parametrize('desc,params,assert_value', query_faq)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--根据分类和机器人Id查询问题分页数据')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    def test_query_faq(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--根据分类和机器人Id查询问题分页数据
        """
        actual_result, expect_result = FaqQuery.faq_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', delete_faq)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--删除')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    @pytest.mark.run(order=1)
    def test_delete_faq(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--删除
        """
        actual_result, expect_result = FaqDelete.faq_delete(self.url,
                                                            params,
                                                            assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', save_faq)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    @pytest.mark.run(order=2)
    def test_save_faq(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--保存
        """
        actual_result, expect_result = FaqSave.faq_save(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', check_question)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--相似性判断--标准问题')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    def test_check_question(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--相似性判断--标准问题
        """
        actual_result, expect_result = FaqCheckQuestion.faq_check_question(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', change_status)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--批量修改状态')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    def test_change_status(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--批量修改状态
        """
        actual_result, expect_result = FaqChangeStatus.faq_change_status(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', change_category)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--批量修改分类')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    def test_change_category(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--批量修改分类
        """
        actual_result, expect_result = FaqChangeCategory.faq_change_category(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', search_page)  # 用例参数化
    @allure.feature("常规问答问答对配置信息")
    @allure.story('常规问答问答对配置信息--模糊查询分页数据')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_faq
    def test_search_page(self, desc, params, assert_value):
        """
        常规问答问答对配置信息--模糊查询分页数据
        """
        actual_result, expect_result = FaqSearchPage.faq_search_page(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)
