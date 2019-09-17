#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
@LastEditTime: 2019-09-17 09:30:55
@LastEditors: Zpp
'''
from flask import Flask
import models
import routes
import services
import logs


def create_app():
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    logs.init_app(app)
    return app


# 初始化
app = create_app()
# print app.url_map
app.run()
