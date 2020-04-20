#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资数据表
@Author: Zpp
@Date: 2020-04-10 13:20:08
@LastEditors: Zpp
@LastEditTime: 2020-04-17 16:33:09
'''

from models import db
import datetime
import json


class Salary(db.Model):
    '''
    工资记录
    '''
    __tablename__ = 'db_salary'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    salary_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    company = db.Column(db.String(255), index=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    id_card = db.Column(db.String(255), index=True, nullable=False)
    phone = db.Column(db.BigInteger, index=True, nullable=False)
    salary = db.Column(db.Text, nullable=False)
    payment_time = db.Column(db.Date, index=True, nullable=False)
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
            dict["payment_time"] = dict["payment_time"].strftime('%Y-%m')
        if "salary" in dict:
            dict["salary"] = json.loads(dict["salary"])
        if "update_time" in dict:
            dict["update_time"] = dict["update_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Salary %r>' % self.salary_id


class SalaryUser(db.Model):
    '''
    员工注册
    '''
    __tablename__ = 'db_salary_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    salary_user_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    id_card = db.Column(db.String(255), index=True, nullable=False, unique=True)
    phone = db.Column(db.BigInteger, index=True, nullable=False, unique=True)
    openid = db.Column(db.String(255), index=True, nullable=False, unique=True)
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
        return '<SalaryUser %r>' % self.salary_user_id


class Attendance(db.Model):
    '''
    考勤记录
    '''
    __tablename__ = 'db_attendance'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    attendance_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    user_id = db.Column(db.String(255), index=True, nullable=False)
    company = db.Column(db.String(255), index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    attance = db.Column(db.Text, nullable=False)
    attendance_time = db.Column(db.Date, index=True, nullable=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    __table_args__ = {
        'useexisting': True,
        'mysql_engine': 'InnoDB'
    }

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "attendance_time" in dict:
            dict["attendance_time"] = dict["attendance_time"].strftime('%Y-%m')
        if "content" in dict:
            dict["content"] = json.loads(dict["content"])
        if "attance" in dict:
            dict["attance"] = json.loads(dict["attance"])
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Attendance %r>' % self.attendance_id
