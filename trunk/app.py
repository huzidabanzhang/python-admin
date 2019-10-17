#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
@LastEditTime: 2019-10-17 14:58:36
@LastEditors: Zpp
'''
from flask import Flask
import models
import routes
import services
import logs
import logging


def create_app():
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app


logs.init_app()
# 初始化
logging.info(u'-----初始化项目-----')
app = create_app()
logging.info('--------------------')

try:
    logging.info(u'------启动成功------')
    app.run()
except Exception as e:
    logging.error(u'------启动失败------')
