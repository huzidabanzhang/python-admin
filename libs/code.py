#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: response返回处理方法
@Author: Zpp
@Date: 2019-09-04 17:09:14
LastEditTime: 2020-11-24 16:54:52
LastEditors: Zpp
'''
from flask import jsonify, request, session
from collection.v1.log import LogModel
from datetime import datetime
import json
import time


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def ResultDeal(code=0, data={}, msg=''):
    response = jsonify(json.loads(json.dumps({
        'code': code,
        'data': data,
        'msg': msg
    }, cls=MyEncoder)))

    if response.headers['Content-Type'] == 'application/json' and response.status_code == 200:
        params = {
            'ip': request.headers['X-Real-Ip'] if 'X-Real-Ip' in request.headers else request.remote_addr,
            'method': request.method,
            'path': request.path,
            'username': session.get('username'),
            'time': GetTimestamp() - session.get('requestTime'),
            'params': request.values.to_dict()
        }

        body = json.loads(response.data)
        if body['code'] == 0:
            params['status'] = 0
            params['content'] = ''
            LogModel().CreateLogRequest(params)
        if body['code'] == -1:
            params['status'] = 1
            params['content'] = body['msg']
            LogModel().CreateLogRequest(params)

    return response


def GetTimestamp():
    now = time.time()
    local_time = time.localtime(now)
    date = str(time.strftime("%Y%m%d%H%M%S", local_time))
    data_secs = (now - int(now)) * 1000
    return int(date + str("%03d" % data_secs))
