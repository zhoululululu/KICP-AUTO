# -*- coding: UTF-8 -*-
'''
Created on 2020/9/7 11:02
@File  : assert_func.py
@author: ZL
@Desc  :
'''

import datetime


class Assert:
    @staticmethod
    def get_result(expected_data, actual_data):
        tf_list = []
        try:
            if len(expected_data) > 1:
                for i in range(len(expected_data)):
                    if expected_data[i] == actual_data[i]:
                        tf_list.append("true")
                    else:
                        tf_list.append("false")
                if set({"true"}) == set(tf_list):
                    return True
                else:
                    return False
            else:
                if expected_data == actual_data:
                    return True
                else:
                    return False
        except Exception as e:
            print(Exception('实际结果与预期结果不一致', expected_data, actual_data))
