#!/usr/bin/env python
# -*- coding:UTF-8 -*-
''' 
@Description: 日志表结构
@Author: Zpp
@Date: 2019-09-12 16:34:07
@LastEditors: Zpp
@LastEditTime: 2019-10-18 11:03:18
'''
from models.base import db
import datetime


class Log(db.Model):
    '''
    日志
    '''
    __tablename__ = 'db_log'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text) # 错误内容
    path = db.Column(db.Text, nullable=False)
    method = db.Column(db.String(36), nullable=False)
    params = db.Column(db.Text) # 请求参数
    ip = db.Column(db.String(255))
    time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, index=True, default=1) # 0 成功 1 失败 2 禁用
    type = db.Column(db.SmallInteger, nullable=False, index=True, default=1) # 0 其他 1 登录
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
