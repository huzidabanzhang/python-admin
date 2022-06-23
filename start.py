#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2019-09-05 16:07:19
LastEditTime: 2022-06-23 10:27:35
LastEditors: Zpp
'''
from flask import Flask
from flask_cors import CORS
from sqlalchemy import Float
# from flask_socketio import SocketIO
from conf.setting import server_info
from libs.utils import IsWindows
import requests
import models
import routes
import services
import logs
import logging
import json


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        origins=['http://localhost:5001', 'https://test.ig132n.cn'],
        supports_credentials=True,
        methods='GET, POST'
    )
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app


logs.init_app()
# 初始化
logging.info('-----初始化项目-----')
app = create_app()
# socketio = SocketIO(app)
# sockets.init_app(socketio)
logging.info('--------------------')


@app.route('/v1/vehicle/info', methods=['GET'], endpoint='getVehicleInfo')
def getVehicleInfo():
    return json.dumps({
        "display_name": "旋风冲锋",
        "latitude": 30.33835,
        "longitude": 121.231738,
        "address": "浙江省宁波市慈溪市滨海四路",
        "usable_battery_level": 61.6,
        "percentage": 80,
        "window": {
            "fd_window": 1,
            "fp_window": 0,
            "rd_window": 1,
            "rp_window": 0
        },
        "locked": False,
        "door": {
            "df": 1,
            "dr": 1,
            "pf": 0,
            "pr": 0
        },
        "inside_temp": 23.8,
        "charging_state": "Disconnected",
        "odometer": 5354,
        "enabled_function": 0
    })


@app.route('/v1/close', methods=['GET', 'POST'], endpoint='handleClose')
def handleClose():

    return json.dumps({
        'outputSpeech': '执行成功, 通风和哨兵模式已关闭'
    })


try:
    logging.info('------启动成功------')
    # if IsWindows():
    #     socketio.run(app, host=server_info['host'], port=server_info['port'])
    # else:
    #     socketio.run(app)
    app.run(debug=IsWindows(), host=server_info['host'], port=server_info['port'])
except Exception as e:
    logging.info(e)
    logging.error('------启动失败------')
