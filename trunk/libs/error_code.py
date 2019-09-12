#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 17:09:14
@LastEditTime: 2019-09-12 11:27:47
@LastEditors: Zpp
'''
from flask import jsonify
import json


def ResultDeal(code=0, data={}, msg=''):
    return jsonify({
        'code': code,
        'data': data,
        'msg': msg
    })
