# -*- coding: UTF-8 -*-
'''
Created on 2020/2/29
@File  : get_config.py
@author: ZL
@Desc  :
'''

import os
import configparser
from selenium import webdriver

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Config:
    def __init__(self):
        """
        初始化config，读取config文件
        """
        self.config = configparser.ConfigParser()
        self.config.read(rootPath + "\\testdata\\config.txt", encoding='UTF-8')
        self.conf = {}

    def get_email_info(self):
        """
        获取email的各种参数配置值
        """
        self.conf['login_email'] = self.config.get("Email", "login_email")
        self.conf['login_password'] = self.config.get("Email", "login_password")
        self.conf['port'] = self.config.get("Email", "port")
        self.conf['smtp'] = self.config.get("Email", "smtp")
        self.conf['Recipient'] = self.config.get("Email", "Recipient")
        self.conf['subject'] = self.config.get("Email", "subject")
        self.conf['mailbody'] = self.config.get("Email", "mailbody")

        return self.conf

    def get_sql_info(self):
        """
        获取数据库的各种参数配置值
        """
        self.conf['db_host'] = self.config.get("Mysql", "db_host")
        self.conf['db_port'] = self.config.get("Mysql", "db_port")
        self.conf['user_name'] = self.config.get("Mysql", "user_name")
        self.conf['user_pwd'] = self.config.get("Mysql", "user_pwd")

        return self.conf


    def get_es_info(self):
        """
        获取ES的各种参数配置值
        """
        self.conf['es_host'] = self.config.get("ES", "ip")
        self.conf['es_port'] = self.config.get("ES", "port")
        self.conf['es_user_name'] = self.config.get("ES", "user_name")
        self.conf['es_user_pwd'] = self.config.get("ES", "user_pwd")

        return self.conf
