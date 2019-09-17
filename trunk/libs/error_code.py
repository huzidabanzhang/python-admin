#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 17:09:14
@LastEditTime: 2019-09-17 10:01:25
@LastEditors: Zpp
'''
from flask import jsonify
from models.log import Log
from models.base import db
import logging


def ResultDeal(code=0, data={}, msg=''):
    return jsonify({
        'code': code,
        'data': data,
        'msg': msg
    })


def RecordLog(src, error):
    logging.exception(error)
    s = db.session()
    item = Log(
        src=src,
        content=error.message
    )
    s.add(item)
    s.commit()
    s.close()
    return str(error.message)
