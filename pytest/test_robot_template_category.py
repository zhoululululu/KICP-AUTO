# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 14:16
@File  : test_robot_template_category.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.templatefaq.faq_query_by_id import FaqQueryById
from api.templatefaq.faq_check_question import FaqCheckQuestion
from api.templatefaq.faq_query_template_category import FaqQueryTemplateCategory
from api.templatefaq.faq_query_template_page import FaqQueryTemplatePage
from api.templatefaq.faq_save_template import FaqSaveTemplate
from api.templatefaq.faq_cite_template import FaqCiteTemplate
from api.templatefaq.faq_query_template_standard_questions import FaqQueryTemplateStandardQuestion
from commonfunc.change_data_type import ChangeDataType
from commonfunc.assert_func import Assert
import os
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class TestRobotTemplateCategory:
    query_faq_template_category = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                                               sheet_name="query_faq_template_category")
    query_template_query_page = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                                             sheet_name="query_template_query_page")
    search_standard_questions = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                                             sheet_name="search_standard_questions")
    save_faq = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                            sheet_name="save_faq")
    cite_faq = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                            sheet_name="cite_faq")
    query_faq_by_id = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                                   sheet_name="query_faq_by_id")
    check_question = ChangeDataType.get_test_data("robotfaq\\faq_template_category.xlsx",
                                                  sheet_name="check_question")

    def setup_class(self):
        self.url = "https://tkf-kicp.kuaishang.cn"

    @pytest.mark.parametrize('desc,params,assert_value', query_faq_template_category)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置问答问答对分类信息--查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_query_faq_template_category(self, desc, params, assert_value):
        """
        预置问答问答对分类信息--查询
        """
        actual_result, expect_result = FaqQueryTemplateCategory.query_template_category(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', query_template_query_page)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置回答问答对配置信息--根据分类和模板Id查询问题分页数据')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_query_template_query_page(self, desc, params, assert_value):
        """
        预置回答问答对配置信息--根据分类和模板Id查询问题分页数据
        """
        actual_result, expect_result = FaqQueryTemplatePage.query_template_page(self.url, params,
                                                                                assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', search_standard_questions)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置回答问答对配置信息--根据分类和模板Id，模糊查询问题/答案分页数据')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_search_standard_questions(self, desc, params, assert_value):
        """
        预置回答问答对配置信息--根据分类和模板Id，模糊查询问题/答案分页数据
        """
        actual_result, expect_result = FaqQueryTemplateStandardQuestion.query_template_standard_question(self.url,
                                                                                                         params,
                                                                                                         assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', save_faq)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置问答问答对分类信息--保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_save_faq(self, desc, params, assert_value):
        """
        预置问答问答对分类信息--保存
        """
        actual_result, expect_result = FaqSaveTemplate.save_template_faq(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', cite_faq)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置问答问答对配置信息--引用')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_cite_faq(self, desc, params, assert_value):
        """
        预置问答问答对配置信息--引用
        """
        actual_result, expect_result = FaqCiteTemplate.cite_template_faq(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', query_faq_by_id)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置回答问答对配置信息--根据ID查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_query_faq_by_id(self, desc, params, assert_value):
        """
        预置回答问答对配置信息--根据ID查询
        """
        actual_result, expect_result = FaqQueryById.query_by_id(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', check_question)  # 用例参数化
    @allure.feature("预置回答问答对配置信息")
    @allure.story('预置问答问答对配置信息--验证标准问题')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.faq_template
    def test_check_question(self, desc, params, assert_value):
        """
        预置问答问答对配置信息--验证标准问题
        """
        actual_result, expect_result = FaqCheckQuestion.check_question_faq(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)
