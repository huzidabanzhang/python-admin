#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2020-02-19 19:45:33
@LastEditTime: 2020-02-19 20:28:39
@LastEditors: Please set LastEditors
'''

from models.base import db
import pandas as pd
import os

class SqlModel():
    def __init__(self):
        self.select = ''

    def read_sql(self):
        