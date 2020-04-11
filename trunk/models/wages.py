#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资数据表
@Author: Zpp
@Date: 2020-04-10 13:20:08
@LastEditors: Zpp
@LastEditTime: 2020-04-10 13:30:17
'''

from models import db
import datetime


class Wages(db.Model):
    '''
    工资记录
    '''
    __tablename__ = 'db_wages'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    wages_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    company = db.Column(db.String(255), index=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    id_card = db.Column(db.String(255), index=True, nullable=False)
    phone = db.Column(db.Integer, index=True, nullable=False)
    wages = db.Column(db.Text, nullable=False)
    payment_time = db.Column(db.DateTime, index=True, nullable=False)
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
        if "payment_time" in dict:
            dict["payment_time"] = dict["payment_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "update_time" in dict:
            dict["update_time"] = dict["update_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Wages %r>' % self.wages_id


class WagesUser(db.Model):
    '''
    员工注册
    '''
    __tablename__ = 'db_wages_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    wages_user_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    id_card = db.Column(db.String(255), index=True, nullable=False)
    phone = db.Column(db.Integer, index=True, nullable=False)
    openid = db.Column(db.String(255), index=True, nullable=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    __table_args__ = {
        'useexisting': True,
        'mysql_engine': 'InnoDB'
    }

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<WagesUser %r>' % self.wages_user_id
