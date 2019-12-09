#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工具
@Author: Zpp
@Date: 2019-10-28 11:28:09
@LastEditors: Zpp
@LastEditTime: 2019-12-09 16:20:17
'''
from models.base import db
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
    except:
        return False
