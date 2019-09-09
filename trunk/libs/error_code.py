# -*- coding:UTF-8 -*-
# trunk/libs/error_code.py
from flask import jsonify
import json


def ResultDeal(code=0, data={}, msg=''):
    return jsonify({
        'code': code,
        'data': data,
        'msg': msg
    })
