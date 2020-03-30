#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-09 10:47:44
@LastEditTime: 2020-03-30 14:56:50
@LastEditors: Zpp
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

class Pool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(Pool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        if options.has_key('pool_size'):
            del options['pool_size']


db = Pool_SQLAlchemy()