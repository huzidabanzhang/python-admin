#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口控制器
@Author: Zpp
@Date: 2019-10-14 13:40:29
@LastEditors  : Zpp
@LastEditTime : 2019-12-23 15:50:06
'''
from flask import request
from models.base import db
from models.system import Interface
from sqlalchemy import text
import uuid


class InterfaceModel():
    def QueryInterfaceByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        接口列表
        '''
        s = db.session()
        try:
            Int = ['menu_id', 'isLock', 'method']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Interface.query.filter_by(**data).filter(
                Interface.name.like("%" + params['name'] + "%") if params.has_key('name') else text('')
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)

    def CreateInterfaceRequest(self, params):
        '''
        新建接口
        '''
        s = db.session()
        try:
            item = Interface(
                interface_id=uuid.uuid4(),
                name=params['name'],
                path=params['path'],
                method=params['method'],
                description=params['description'],
                menu_id=params['menu_id'],
                identification=params['identification']
            )
            s.add(item)
            s.commit()
            return item
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetInterfaceRequest(self, interface_id):
        '''
        查询接口
        '''
        s = db.session()
        try:
            interface = s.query(Interface).filter(Interface.interface_id == interface_id).first()
            if not interface:
                return str('接口不存在')

            return interface.to_json()
        except Exception as e:
            print e
            return str(e.message)

    def ModifyInterfaceRequest(self, interface_id, params):
        '''
        修改接口信息
        '''
        s = db.session()
        try:
            interface = s.query(Interface).filter(Interface.interface_id == interface_id).first()
            if not interface:
                return str('接口不存在')

            AllowableFields = ['name', 'path', 'method', 'description', 'menu_id', 'identification']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Interface).filter(Interface.interface_id == interface_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockInterfaceRequest(self, interface_id, isLock):
        '''
        禁用接口
        '''
        s = db.session()
        try:
            s.query(Interface).filter(Interface.interface_id.in_(interface_id)).update({Interface.isLock: isLock}, synchronize_session=False)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
