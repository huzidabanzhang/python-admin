#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
@LastEditTime: 2019-10-15 09:48:37
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


@app.errorhandler(401)
def handle_401_error(error):
    return u'登录认证失效，请重新登录'


@app.errorhandler(403)
def handle_403_error(error):
    return u'您没有访问权限'


@app.errorhandler(404)
def handle_404_error(error):
    return u'页面不存在'


@app.errorhandler(405)
def handle_404_error(error):
    return u'方法不被允许'


@app.errorhandler(500)
def handle_500_error(error):
    return u'服务器错误 %s' % error


try:
    logging.info(u'------启动成功------')
    app.run()
except Exception as e:
    logging.error(u'------启动失败------')
