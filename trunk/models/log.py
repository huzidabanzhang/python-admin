#!/usr/bin/env python
# -*- coding:UTF-8 -*-
''' 
@Description: 日志表结构
@Author: Zpp
@Date: 2019-09-12 16:34:07
@LastEditors: Zpp
@LastEditTime: 2019-09-12 16:37:33
'''
from models.base import db
import datetime


class Log(db.Model):
    '''
    日志
    '''
    __tablename__ = 'db_log'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    content = db.Column(db.String(), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Log %r>' % self.id
