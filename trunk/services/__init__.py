#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 10:23:44
@LastEditTime: 2019-09-12 11:29:13
@LastEditors: Zpp
'''
from conf.setting import server_info, token_info


def init_app(app):
    # 启动服务
    app.config.from_object(server_info)
    # session
    app.config['SECRET_KEY'] = token_info['SECRET_KEY']
    # 调试模式
    app.config['DEBUG'] = True
