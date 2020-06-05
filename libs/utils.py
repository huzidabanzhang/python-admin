#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工具
@Author: Zpp
@Date: 2019-10-28 11:28:09
@LastEditors: Zpp
@LastEditTime: 2020-06-05 16:07:57
'''
import platform


def isWindows():
    return True if platform.system() == 'Windows' else False


def readFile(path, type='r'):
    f = open(path, type)
    content = f.read()
    f.close()
    return content
