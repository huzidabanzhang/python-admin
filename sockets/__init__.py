#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: SocketIO配置
@Author: Zpp
@Date: 2020-05-19 14:43:38
@LastEditors: Zpp
@LastEditTime: 2020-05-19 17:29:45
'''
from flask_socketio import emit, Namespace


class MyCustomNamespace(Namespace):
    def on_connect(self):
        emit('my_response', {'data': 'Connected'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_my_event(self, data):
        emit('my_response', data)


def init_app(socketio):
    socketio.on_namespace(MyCustomNamespace('/'))
