#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
@LastEditTime: 2019-09-17 14:37:06
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
    logs.init_app(app)
    return app


# 初始化
app = create_app()

if not app.config['DEBUG']:
    logging.info(u'启动')
# print app.url_map
app.run()
