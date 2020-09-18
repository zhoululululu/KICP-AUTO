# -*- coding: UTF-8 -*-
'''
Created on 2020/9/10 14:42
@File  : get_es_connect.py
@author: ZL
@Desc  :
'''

from commonfunc.get_config import Config
from elasticsearch import Elasticsearch


class ElasticConnect:
    def __init__(self, index_name):
        '''
        连接es
        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.config = Config()
        self.c = self.config.get_es_info()
        self.es_host = self.c["es_host"]
        self.es_port = int(self.c["es_port"])
        self.es_user_name = self.c["es_user_name"]
        self.es_user_pwd = self.c["es_user_pwd"]
        self.index_name = index_name
        self.es = Elasticsearch([self.es_host], http_auth=(self.es_user_name, self.es_user_pwd), port=self.es_port)

    def get_search(self, query_body):
        _searched = self.es.search(index=self.index_name, body=query_body)
        return _searched

