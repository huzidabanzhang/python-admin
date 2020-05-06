#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工具
@Author: Zpp
@Date: 2019-10-28 11:28:09
@LastEditors: Zpp
@LastEditTime: 2020-05-06 09:59:55
'''
import platform


def isWindows():
    return True if platform.system() == 'Windows' else False


def readFile(path, type):
    f = open(path, type)
    content = f.read()
    f.close()
    return content
