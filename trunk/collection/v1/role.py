#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限控制器
@Author: Zpp
@Date: 2019-09-10 16:01:46
@LastEditTime: 2020-05-06 17:22:43
@LastEditors: Zpp
'''
from flask import request
from models import db
from models.system import Role, Interface, Menu
from sqlalchemy import text
from libs.scope import isExists
import uuid
import json


class RoleModel():
    def __init__(self):
        self.exists = {
            'name': u'角色名称',
            'mark': u'标识'
        }

    def isCreateExists(self, s, params):
        '''
        判断新增时记录是否存在
        '''
        d = {}
        for i in self.exists:
            d[i] = {
                'value': params[i],
                'name': self.exists[i]
            }

        return isExists(s, Role, d)

    def isSaveExists(self, s, params, data):
        '''
        判断修改时记录是否存在
        '''
        d = {}
        for i in self.exists:
            if params.has_key(i) and params[i] != data.__dict__[i]:
                d[i] = {
                    'value': params[i],
                    'name': self.exists[i]
                }

        return isExists(s, Role, d)

    def CreateRoleRequest(self, params):
        '''
        新建权限
        '''
        s = db.session()
        is_exists = self.isCreateExists(s, params)

        if is_exists != True:
            return str(is_exists['error'].encode('utf8'))

        try:
            item = Role(
                name=params['name'],
                mark=params['mark'],
                role_id=uuid.uuid4(),
                is_disabled=params['is_disabled'],
                role_list=json.dumps(params['role_list'])
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetRoleRequest(self, role_id):
        '''
        查询权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            return role.to_json()
        except Exception as e:
            print e
            return str(e.message)

    def ModifyRoleRequest(self, role_id, params):
        '''
        修改权限信息
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            is_exists = self.isSaveExists(s, params, role)

            if is_exists != True:
                return str(is_exists['error'].encode('utf8'))

            role.name = params['name']
            role.mark = params['mark']
            role.is_disabled = params['is_disabled']
            role.role_list = json.dumps(params['role_list'])
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockRoleRequest(self, role_id, is_disabled):
        '''
        禁用权限
        '''
        s = db.session()
        try:
            s.query(Role).filter(Role.role_id.in_(role_id)).update({Role.is_disabled: is_disabled}, synchronize_session=False)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelRoleRequest(self, role_id):
        '''
        删除权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id.in_(role_id)).all()
            for i in role:
                s.delete(i)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def QueryRoleByParamRequest(self, params):
        '''
        权限列表
        '''
        s = db.session()
        try:
            data = {}
            if params.has_key('is_disabled'):
                data['is_disabled'] = params['is_disabled']

            result = Role.query.filter_by(**data).order_by(Role.id).all()

            data = []
            for value in result:
                data.append(value.to_json())

            return data
        except Exception as e:
            print e
            return str(e.message)
