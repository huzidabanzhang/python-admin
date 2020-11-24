#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工具
@Author: Zpp
@Date: 2019-10-28 11:28:09
LastEditors: Zpp
LastEditTime: 2020-11-24 16:27:50
'''
import platform


def IsWindows():
    return True if platform.system() == 'Windows' else False


def ReadFile(path, type='r'):
    try:
        f = open(path, type)
        content = f.read()
        f.close()
        return content
    except:
        return False


def WriteFile(path, content, type='w'):
    try:
        f = open(path, type)
        f.write(content)
        f.close()
        return True
    except:
        return False


def health_database_status(s, sql):
    is_db = True

    try:
        s.execute(sql)
    except:
        is_db = False

    return is_db
