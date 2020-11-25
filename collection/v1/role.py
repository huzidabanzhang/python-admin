#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 鉴权控制器
@Author: Zpp
@Date: 2019-09-10 16:01:46
@LastEditTime: 2020-05-29 14:37:31
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
            'name': '角色名称',
            'mark': '标识'
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
            if i in params and params[i] != data.__dict__[i]:
                d[i] = {
                    'value': params[i],
                    'name': self.exists[i]
                }

        return isExists(s, Role, d)

    def CreateRoleRequest(self, params):
        '''
        新建鉴权
        '''
        s = db.session()
        is_exists = self.isCreateExists(s, params)

        if is_exists != True:
            return str(is_exists['error'].encode('utf8'))

        try:
            item = Role(
                name=params['name'],
                mark=params['mark'],
                role_id=str(uuid.uuid4()),
                disable=params['disable'],
                role_list=json.dumps({
                    'I': params.getlist('role_list[]'),
                    'M': params.getlist('menu[]')
                })
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print(e)
            return str(e)

    def GetRoleRequest(self, role_id):
        '''
        查询鉴权
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            return role.to_json()
        except Exception as e:
            print(e)
            return str(e)

    def ModifyRoleRequest(self, role_id, params):
        '''
        修改鉴权信息
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
            role.disable = params['disable']
            role.role_list = json.dumps({
                'I': params.getlist('role_list[]'),
                'M': params.getlist('menu[]')
            })
            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

    def LockRoleRequest(self, role_id, disable):
        '''
        禁用鉴权
        '''
        s = db.session()
        try:
            s.query(Role).filter(Role.role_id.in_(role_id)).update({Role.disable: disable}, synchronize_session=False)
            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

    def DelRoleRequest(self, role_id):
        '''
        删除鉴权
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id.in_(role_id)).all()
            for i in role:
                s.delete(i)
            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

    def QueryRoleByParamRequest(self, params):
        '''
        鉴权列表
        '''
        s = db.session()
        try:
            data = {}
            if 'disable' in params:
                data['disable'] = params['disable']

            result = Role.query.filter_by(**data).order_by(Role.id).all()

            data = []
            for value in result:
                data.append(value.to_json())

            return data
        except Exception as e:
            print(e)
            return str(e)
