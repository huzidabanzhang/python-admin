#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
@LastEditTime: 2019-09-12 11:29:26
@LastEditors: Zpp
'''
from flask import Flask
import models
import routes
import services


def create_app():
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app


# 初始化
app = create_app()
# print app.url_map
app.run()
