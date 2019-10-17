#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: response返回处理方法
@Author: Zpp
@Date: 2019-09-04 17:09:14
@LastEditTime: 2019-10-17 14:51:24
@LastEditors: Zpp
'''
from flask import jsonify


def ResultDeal(code=0, data={}, msg=''):
    return jsonify({
        'code': code,
        'data': data,
        'msg': msg
    })
