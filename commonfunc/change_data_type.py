# -*- coding: UTF-8 -*-
'''
Created on 2020/2/26
@File  : change_data_type.py
@author: ZL
@Desc  :
'''

import json
import pandas
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class ChangeDataType:

    @staticmethod
    def file_to_dict(path, sheet_name=None):
        test_data = []
        form = str(path).split(".")[-1]
        try:
            if form == "txt":
                f = open(path, "r")
                for line in f.readlines():
                    test_data.append(line.strip("\n"))
            elif form == "csv":
                test_data = pandas.read_csv(path, encoding="utf-8")
            elif form == "xls" or form == "xlsx":
                test_data = pandas.read_excel(path, sheet_name=sheet_name, encoding="utf-8")
                return test_data
            elif form == "json":
                with open(path, mode='r', encoding='utf-8') as f2:
                    test_data = json.load(f2)
        except FileNotFoundError as fe:
            print("文件不存在，请检查文件名", fe)
        except AttributeError as ae:
            print("方法不存在，请检查方法名", ae)
        except Exception as e:
            print(e)
        return test_data

    def get_test_data(file, sheet_name=None):
        all_data = ChangeDataType.file_to_dict(rootPath + "\\testdata\\" + file, sheet_name=sheet_name)
        description = all_data.description.tolist()
        params = all_data.data.tolist()
        assert_value = all_data.assert_value.tolist()
        result = []
        for i in range(len(params)):
            result.append((description[i], params[i], assert_value[i]))
        return result
