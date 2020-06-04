#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口控制器
@Author: Zpp
@Date: 2019-10-14 13:40:29
@LastEditors: Zpp
@LastEditTime: 2020-05-29 16:37:50
'''
from flask import request
from models import db
from models.system import Interface, Menu
from sqlalchemy import text
from libs.scope import isExists
import uuid
import copy


class InterfaceModel():
    def __init__(self):
        self.exists = {
            'name': u'接口名称',
            'path': u'路由',
            'mark': u'标识'
        }

    def isCreateExists(self, s, params):
        '''
        判断记录是否存在
        '''
        d = {}
        for i in self.exists:
            d[i] = {
                'value': params[i],
                'name': self.exists[i]
            }

        return isExists(s, Interface, d)

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

        return isExists(s, Interface, d)

    def QueryInterfaceByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        接口列表
        '''
        s = db.session()
        try:
            Int = ['menu_id', 'disable', 'method']
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
        is_exists = self.isCreateExists(s, params)

        if is_exists != True:
            return str(is_exists['error'].encode('utf8'))

        try:
            menus = s.query(Menu).filter(Menu.menu_id.in_(params.getlist('menus[]'))).all()

            item = Interface(
                interface_id=uuid.uuid4(),
                name=params['name'],
                path=params['path'],
                method=params['method'],
                description=params['description'],
                mark=params['mark'],
                forbid=params['forbid'],
                disable=params['disable'],
                menus=menus
            )
            s.add(item)
            data = copy.deepcopy(item.to_json())
            s.commit()
            return data
        except Exception as e:
            s.rollback()
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

            AllowableFields = ['name', 'path', 'method', 'description', 'disable']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            is_exists = self.isSaveExists(s, data, interface)

            if is_exists != True:
                return str(is_exists['error'].encode('utf8'))

            menus = s.query(Menu).filter(Menu.menu_id.in_(params.getlist('menus[]'))).all()
            interface.menus = menus
            s.query(Interface).filter(Interface.interface_id == interface_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockInterfaceRequest(self, interface_id, disable):
        '''
        禁用接口
        '''
        s = db.session()
        try:
            s.query(Interface).filter(Interface.interface_id.in_(interface_id)).update({Interface.disable: disable}, synchronize_session=False)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelInterfaceRequest(self, interface_id):
        '''
        删除接口
        '''
        s = db.session()
        try:
            result = s.query(Interface).filter(Interface.interface_id.in_(interface_id)).all()
            for i in result:
                s.delete(i)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
