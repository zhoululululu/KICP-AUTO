# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 14:16
@File  : test_robot_faq_category.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.categoryfaq.faq_delete_category import FaqDeleteCategory
from api.categoryfaq.faq_query_category import FaqQueryCategory
from api.categoryfaq.faq_save_category import FaqSaveCategory
from api.categoryfaq.faq_update_index_no import FaqUpdateIndexNo
from commonfunc.change_data_type import ChangeDataType
from commonfunc.assert_func import Assert
import os
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class TestRobotFaqCategory:
    query_category = ChangeDataType.get_test_data("robotfaq\\faq_robot_category.xlsx",
                                                  sheet_name="query_category")
    save_category = ChangeDataType.get_test_data("robotfaq\\faq_robot_category.xlsx",
                                                 sheet_name="save_category")
    delete_category = ChangeDataType.get_test_data("robotfaq\\faq_robot_category.xlsx",
                                                   sheet_name="delete_category")
    update_index_no = ChangeDataType.get_test_data("robotfaq\\faq_robot_category.xlsx",
                                                   sheet_name="update_index_no")

    def setup_class(self):
        self.url = "https://tkf-kicp.kuaishang.cn"

    @pytest.mark.parametrize('desc,params,assert_value', query_category)  # 用例参数化
    @allure.feature("常规问答问答对分类信息")
    @allure.story('常规问答问答对分类信息--查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.category_faq
    def test_query_category(self, desc, params, assert_value):
        """
        常规问答问答对分类信息--查询
        """
        actual_result, expect_result = FaqQueryCategory.faq_query_category(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', save_category)  # 用例参数化
    @allure.feature("常规问答问答对分类信息")
    @allure.story('常规问答问答对分类信息--保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.category_faq
    def test_save_category(self, desc, params, assert_value):
        """
        常规问答问答对分类信息--保存
        """
        actual_result, expect_result = FaqSaveCategory.faq_save_category(self.url, params,
                                                                         assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', delete_category)  # 用例参数化
    @allure.feature("常规问答问答对分类信息")
    @allure.story('常规问答问答对分类信息--删除')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.category_faq
    def test_delete_category(self, desc, params, assert_value):
        """
        常规问答问答对分类信息--删除
        """
        actual_result, expect_result = FaqDeleteCategory.delete_category_faq(self.url,
                                                                             params,
                                                                             assert_value)
        assert Assert.get_result(actual_result, expect_result)

    @pytest.mark.parametrize('desc,params,assert_value', update_index_no)  # 用例参数化
    @allure.feature("常规问答问答对分类信息")
    @allure.story('常规问答问答对分类信息--修改排序')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.category_faq
    def test_update_index_no(self, desc, params, assert_value):
        """
        常规问答问答对分类信息--修改排序
        """
        actual_result, expect_result = FaqUpdateIndexNo.update_index_no_faq(self.url, params, assert_value)
        assert Assert.get_result(actual_result, expect_result)
