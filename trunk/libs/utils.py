#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工具
@Author: Zpp
@Date: 2019-10-28 11:28:09
@LastEditors  : Please set LastEditors
@LastEditTime : 2020-02-14 15:45:41
'''
from models import db
from models.system import InitSql


def readFile(path, type):
    f = open(path, type)
    content = f.read()
    f.close()
    return content


def checkDb():
    try:
        s = db.session()
        res = s.query(InitSql).first()
        return res.isInit
    except Exception as e:
        return str('数据库未连接或者其他错误请查看错误信息：' + e.message)
