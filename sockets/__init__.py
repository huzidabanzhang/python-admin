#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: SocketIO配置
@Author: Zpp
@Date: 2020-05-19 14:43:38
@LastEditors: Zpp
@LastEditTime: 2020-05-21 16:12:45
'''
from flask import request
from flask_socketio import emit, Namespace

client = []


class MyCustomNamespace(Namespace):
    def on_error(self, e):
        print(e)

    def on_error_default(self, e):
        print(e)

    def on_connect(self):
        client.append(request.sid)
        print(client)
        emit('my_response', '连接成功')

    def on_disconnect(self):
        sid = request.sid
        if sid in client:
            client.remove(sid)
        print(client)

    def on_heart(self, data):
        print(data)
        emit('heart', 'server')

    def on_my_response(self, data):
        print(data)


def init_app(socketio):
    socketio.on_namespace(MyCustomNamespace('/'))
