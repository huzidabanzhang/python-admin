#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 10:23:44
@LastEditTime: 2019-09-17 14:28:18
@LastEditors: Zpp
'''
from flask_session import Session
from flask_compress import Compress
from flask_cache import Cache
from conf.setting import server_info, token_info, session_info, cache_info


def init_app(app):
    # 启动服务配置
    app.config.from_object(server_info)
    # 密钥
    app.config['SECRET_KEY'] = token_info['SECRET_KEY']
    # 调试模式
    app.config['DEBUG'] = True
    # SESSION配置
    app.config.update(session_info)
    # CACHE配置
    app.config.update(cache_info)

    Session(app)
    Cache(app)
    Compress(app)
    return app
