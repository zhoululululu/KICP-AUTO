# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 14:16
@File  : test_robot_manage.py
@author: ZL
@Desc  :
'''
import pytest
import allure
from api.robotmanage.robot_query import RobotQuery
from api.robotmanage.robot_add import RobotAdd
from api.robotmanage.robot_detail import RobotDetail
from api.robotmanage.robot_template_list import RobotTemplateList
from api.robotmanage.robot_plan_list import RobotPlanList
from api.robotmanage.robot_delete import RobotDelete
from api.robotmanage.robot_edit import RobotEdit
from api.robotmanage.robot_login import RobotLogin
from api.robotmanage.robot_set_status import RobotSetStatus
from commonfunc.change_data_type import ChangeDataType
from commonfunc.assert_func import Assert
import os
import json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0].split("api")[0]


class TestRobotManage:
    query_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="query_data")
    add_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="add_data")
    detail_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="detail_data")
    edit_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="edit_data")
    delete_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="delete_data")
    set_status_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="set_status_data")
    login_robot_data = ChangeDataType.get_test_data("robotmanage\\robot_manage.xlsx", sheet_name="login_data")

    def setup_class(self):
        self.url = "https://tkf-kicp.kuaishang.cn"

    @pytest.mark.parametrize('desc,params,assert_value', query_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('查询机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_query(self, desc, params, assert_value):
        """
        查询robot
        """
        (actual_result, except_result) = RobotQuery.query_robot(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', add_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('新增机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_add(self, desc, params, assert_value):
        """
        新增robot
        """
        (actual_result, except_result) = RobotAdd.add_robot(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', detail_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('机器人详情')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_detail(self, desc, params, assert_value):
        """
        详情robot
        """
        (actual_result, except_result) = RobotDetail.detail_robot(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', edit_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('编辑机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_edit(self, desc, params, assert_value):
        """
        编辑robot
        """
        (actual_result, except_result) = RobotEdit.edit_robot(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', set_status_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('开启/停用机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_set_status(self, desc, params, assert_value):
        """
        开启/停用robot
        """
        (actual_result, except_result) = RobotSetStatus.set_status_robot(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', delete_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('删除机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_delete(self, desc, params, assert_value):
        """
        删除robot
        """
        (actual_result, except_result) = RobotDelete.delete_robot(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', login_robot_data)  # 用例参数化
    @allure.feature("机器人管理")
    @allure.story('登录机器人')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_login(self, desc, params, assert_value):
        """
        登录robot
        """
        (actual_result, except_result) = RobotLogin.login_robot(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @allure.feature("机器人管理")
    @allure.story('机器人模板列表')  # 描述
    @allure.title('机器人模板列表-无参数直接校验')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_template_list(self):
        """
        templateList-无参数直接校验
        """
        (actual_result, except_result) = RobotTemplateList.template_list(self.url)
        assert Assert.get_result(actual_result, except_result)

    @allure.feature("机器人管理")
    @allure.story('机器人套餐列表')  # 描述
    @allure.title('机器人套餐列表-无参数直接校验')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_plan_list(self):
        """
        planList-无参数直接校验
        """
        (actual_result, except_result) = RobotPlanList.plan_list(self.url)
        assert Assert.get_result(actual_result, except_result)

    @allure.feature("机器人管理")
    @allure.story('上传机器人头像')  # 描述
    @allure.title('上传机器人头像-无额外校验')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_manage
    def test_robot_plan_list(self):
        """
        planList-无参数直接校验
        """
        (actual_result, except_result) = RobotPlanList.plan_list(self.url)
        assert Assert.get_result(actual_result, except_result)
