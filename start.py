#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-05 16:07:19
LastEditTime: 2020-11-24 14:10:40
LastEditors: Zpp
'''
from flask import Flask
from flask_socketio import SocketIO
from conf.setting import server_info
from libs.utils import IsWindows
import sockets
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
logging.info('-----初始化项目-----')
app = create_app()
socketio = SocketIO(app)
sockets.init_app(socketio)
logging.info('--------------------')

try:
    logging.info('------启动成功------')
    if IsWindows():
        socketio.run(app, host=server_info['host'], port=server_info['port'])
    else:
        socketio.run(app)
except Exception as e:
    print(e)
    logging.error('------启动失败------')
