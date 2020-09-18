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
from api.robotconfig.robot_greeting_save import RobotGreetingsave
from api.robotconfig.robot_warm_word_query import RobotWarmWordQuery
from api.robotconfig.robot_warm_word_save import RobotWarmWordSave
from api.robotconfig.robot_un_problem_query import RobotUnProblemQuery
from api.robotconfig.robot_un_problem_save import RobotUnProblemSave
from api.robotconfig.robot_guide_query import RobotGuideQuery
from api.robotconfig.robot_guide_save import RobotGuideSave
from api.robotconfig.robot_advance_settings_query import RobotAdvanceSettingsQuery
from api.robotconfig.robot_advance_settings_save import RobotAdvanceSettingsSave
from api.robotconfig.robot_artiticial_settings_query import RobotArtiticialSettingsQuery
from api.robotconfig.robot_artiticial_settings_save import RobotArtiticialSettingsSave
from api.robotconfig.robot_guest_settings_query import RobotGuestSettingsQuery
from api.robotconfig.robot_guest_settings_save import RobotGuestSettingsSave
from api.robotconfig.robot_hot_question_query import RobotHotQuestionQuery
from api.robotconfig.robot_hot_question_save import RobotHotQuestionSave
from api.robotconfig.robot_want_toask_query import RobotWantToaskQuery
from api.robotconfig.robot_want_toask_save import RobotWantToaskSave
from api.robotconfig.robot_related_question_query import RobotRelatedQuestionQuery
from api.robotconfig.robot_related_question_save import RobotRelatedQuestionSave
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
    greeting_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                      sheet_name="save_greeting")
    guide_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                   sheet_name="save_guide")
    warm_word_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                       sheet_name="save_warm_word")
    un_problem_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                        sheet_name="save_unproblem")
    guest_settings_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                             sheet_name="query_guest_settings")
    guest_settings_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                            sheet_name="save_guest_settings")
    artificial_settings_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                                  sheet_name="query_artificial_settings")
    artificial_settings_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                                 sheet_name="save_artiticial_settings")
    advance_settings_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                               sheet_name="query_advance_settings")
    advance_settings_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                              sheet_name="save_advance_settings")
    want_toask_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                         sheet_name="query_want_toask")
    want_toask_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                        sheet_name="save_want_toask")
    related_question_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                               sheet_name="query_related_question")
    related_question_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                              sheet_name="save_related_question")
    hot_question_query_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                           sheet_name="query_hot_question")
    hot_question_save_data = ChangeDataType.get_test_data("robotconfig\\robot_config.xlsx",
                                                          sheet_name="save_hot_question")

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

    @pytest.mark.parametrize('desc,params,assert_value', greeting_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人问候语保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_greeting_save(self, desc, params, assert_value):
        """
        机器人问候语保存
        """
        actual_result, except_result = RobotGreetingsave.greeting_save(self.url, json.loads(params), assert_value)
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

    @pytest.mark.parametrize('desc,params,assert_value', greeting_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人欢迎语保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_greeting_save(self, desc, params, assert_value):
        """
        机器人欢迎语保存
        """
        actual_result, except_result = RobotGreetingsave.greeting_save(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', greeting_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人欢迎语查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_greeting_query(self, desc, params, assert_value):
        """
        机器人欢迎语查询
        """
        actual_result, except_result = RobotGreetingQuery.greeting_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', guide_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人引导语保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_guide_save(self, desc, params, assert_value):
        """
        机器人引导语保存
        """
        actual_result, except_result = RobotGuideSave.guide_save(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', warm_word_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人暖场语保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_warm_word_save(self, desc, params, assert_value):
        """
        机器人暖场语保存
        """
        actual_result, except_result = RobotWarmWordSave.warm_word_save(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', un_problem_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人未知问题语保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_unproblem_save(self, desc, params, assert_value):
        """
        机器人未知问题保存
        """
        actual_result, except_result = RobotUnProblemSave.un_problem_save(self.url, json.loads(params), assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', guest_settings_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人访客端查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=1)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_guest_settings_query(self, desc, params, assert_value):
        """
        机器人机器人访客端查询
        """
        actual_result, except_result = RobotGuestSettingsQuery.guest_settings_query(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', guest_settings_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人访客端保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_guest_settings_save(self, desc, params, assert_value):
        """
        机器人访客端保存
        """
        actual_result, except_result = RobotGuestSettingsSave.guest_settings_save(self.url, params, assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', artificial_settings_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人转人工设置查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_artificial_settings_query(self, desc, params, assert_value):
        """
        机器人转人工设置查询
        """
        actual_result, except_result = RobotArtiticialSettingsQuery.artiticial_settings_query(self.url, params,
                                                                                              assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', artificial_settings_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人转人工设置保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_artificial_settings_save(self, desc, params, assert_value):
        """
        机器人转人工设置保存
        """
        actual_result, except_result = RobotArtiticialSettingsSave.artiticial_settings_save(self.url, params,
                                                                                            assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', advance_settings_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人高级设置查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_advance_settings_query(self, desc, params, assert_value):
        """
        机器人高级设置查询
        """
        actual_result, except_result = RobotAdvanceSettingsQuery.advance_settings_query(self.url, params,
                                                                                        assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', advance_settings_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人高级设置保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_advance_settings_save(self, desc, params, assert_value):
        """
        机器人高级设置保存
        """
        actual_result, except_result = RobotAdvanceSettingsSave.advance_settings_save(self.url, params,
                                                                                      assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', want_toask_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人猜你想问查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_want_toask_query(self, desc, params, assert_value):
        """
        机器人猜你想问查询
        """
        actual_result, except_result = RobotWantToaskQuery.want_toask_query(self.url, params,
                                                                            assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', want_toask_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人猜你想问保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_want_toask_save(self, desc, params, assert_value):
        """
        机器人猜你想问保存
        """
        actual_result, except_result = RobotWantToaskSave.want_toask_save(self.url, params,
                                                                          assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', related_question_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人关联问题查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_related_related_question_query(self, desc, params, assert_value):
        """
        机器人关联问题查询
        """
        actual_result, except_result = RobotRelatedQuestionQuery.related_question_query(self.url, params,
                                                                                        assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', related_question_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人关联问题保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_related_question_save(self, desc, params, assert_value):
        """
        机器人关联问题保存
        """
        actual_result, except_result = RobotRelatedQuestionSave.related_question_save(self.url, params,
                                                                                      assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', hot_question_query_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人热点问题查询')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_hot_question_query(self, desc, params, assert_value):
        """
        机器人热点问题查询
        """
        actual_result, except_result = RobotHotQuestionQuery.hot_question_query(self.url, params,
                                                                                assert_value)
        assert Assert.get_result(actual_result, except_result)

    @pytest.mark.parametrize('desc,params,assert_value', hot_question_save_data)  # 用例参数化
    @allure.feature("机器人配置")
    @allure.story('机器人热点问题保存')  # 描述
    @allure.title('{desc}')  # title
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.robot_config
    def test_robot_hot_question_save(self, desc, params, assert_value):
        """
        机器人热点问题保存
        """
        actual_result, except_result = RobotHotQuestionSave.hot_question_save(self.url, params,
                                                                              assert_value)
        assert Assert.get_result(actual_result, except_result)
