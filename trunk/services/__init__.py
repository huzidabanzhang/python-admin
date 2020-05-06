#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 10:23:44
@LastEditTime: 2020-05-06 10:05:36
@LastEditors: Zpp
'''
from flask_session import Session
from flask_compress import Compress
from flask_cache import Cache
from conf.setting import token_info, session_info, cache_info
from libs.utils import isWindows

cache = Cache()

def init_app(app):
    # 密钥
    app.config['SECRET_KEY'] = token_info['SECRET_KEY']
    # 调试模式
    app.config['DEBUG'] = isWindows()
    # SESSION配置
    app.config.update(session_info)
    # CACHE配置
    app.config.update(cache_info)

    Session(app)
    Compress(app)
    global cache
    cache.init_app(app)
