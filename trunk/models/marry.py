#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 记录结婚相关的表
@Author: Zpp
@Date: 2020-03-18 16:15:56
@LastEditors: Zpp
@LastEditTime: 2020-03-31 09:37:34
'''

from models import db
import datetime


class Renovation(db.Model):
    '''
    装修记录
    '''
    __tablename__ = 'db_renovation'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    renovation_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    pid = db.Column(db.String(36), nullable=False, index=True, default='0')
    name = db.Column(db.String(36), index=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    __table_args__ = {
        'useexisting': True,
        'mysql_engine': 'InnoDB'
    }

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "update_time" in dict:
            dict["update_time"] = dict["update_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Renovation %r>' % self.name
