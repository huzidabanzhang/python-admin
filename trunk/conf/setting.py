#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 基本配置信息
@Author: Zpp
@Date: 2019-09-02 15:53:39
@LastEditTime: 2019-09-17 14:17:08
@LastEditors: Zpp
'''
import hashlib
import os

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')

token_info = {
    'expiration': 30 * 24 * 3600,
    'SECRET_KEY': 'k#6@1%8)a'
}

# 启动服务参数 字典类型
server_info = {
    "host": '0.0.0.0',
    "port": 5000,  # 启动服务的端口号
}

# 日志
log_info = {
    'LOG_FILE_BACKUP_COUNT': 0,
    'LOG_PATH_ERROR': os.path.join(os.path.join(basedir, 'logs'), 'error.log'),
    'LOG_PATH_INFO': os.path.join(os.path.join(basedir, 'logs'), 'info.log')
}

# session参数
session_info = {
    'SESSION_TYPE': 'filesystem',
    'SESSION_FILE_DIR': os.path.join(basedir, 'sessions'),
    'SESSION_FILE_THRESHOLD': 500,
    'SESSION_FILE_MODE': 384
}

# cache参数
cache_info = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': os.path.join(basedir, 'caches'),
    'CACHE_THRESHOLD': 500
}


class Config():
    def __init__(self):
        # mysql 配置信息
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = 'intersky'
        self.db = 'flask'
        self.charset = 'utf8'

    def get_sql_url(self):
        return "mysql://%s:%s@%s:%s/%s?charset=utf8" % (self.user, self.password, self.host, self.port, self.db)

    def get_md5(self, m):
        h = hashlib.md5()
        h.update(m.encode('utf-8'))
        return h.hexdigest()
