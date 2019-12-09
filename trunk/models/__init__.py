#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 10:23:51
@LastEditTime: 2019-12-09 15:38:30
@LastEditors: Zpp
'''
from conf.setting import Config
from base import db


def init_app(app):
    # mysql 数据库连接数据
    app.config['SQLALCHEMY_DATABASE_URI'] = Config().get_sql_url()
    # 禁用追踪对象的修改并且发送信号（会需要额外内存）
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
