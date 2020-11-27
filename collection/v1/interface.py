#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口控制器
@Author: Zpp
@Date: 2019-10-14 13:40:29
LastEditors: Zpp
LastEditTime: 2020-11-26 16:00:42
'''
from flask import request
from models import db
from models.system import Interface, Menu, Role
from sqlalchemy import text
from libs.scope import isExists
import uuid
import copy


class InterfaceModel():
    def __init__(self):
        self.exists = {
            'name': '接口名称',
            'path': '路由',
            'mark': '标识'
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
            if i in params and params[i] != data.__dict__[i]:
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
            data = {}
            for i in ['disable', 'method']:
                if i in params:
                    data[i] = params[i]

            menus = text('')
            if 'menu_id' in params:
                menus = Interface.menu.any(Menu.menu_id == params['menu_id'])

            roles = text('')
            if 'role_id' in params:
                roles = Interface.role.any(Role.role_id == params['role_id'])

            result = Interface.query.filter_by(**data).filter(
                Interface.name.like("%" + params['name'] + "%") if 'name' in params else text(''),
                menus,
                roles
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            items = []
            for i in result.items:
                menus = [{
                    'name': m.title,
                    'menu_id': m.menu_id
                } for m in i.menus]
                roles = [{
                    'name': r.name,
                    'role_id': r.role_id
                } for r in i.roles]
                item = i.to_json()
                item['menus'] = menus
                item['roles'] = roles
                items.append(item)

            return {'data': items, 'total': result.total}
        except Exception as e:
            print(e)
            return str(e)

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
            roles = s.query(Role).filter(Role.role_id.in_(params.getlist('roles[]'))).all()

            item = Interface(
                interface_id=str(uuid.uuid4()),
                name=params['name'],
                path=params['path'],
                method=params['method'],
                description=params['description'],
                mark=params['mark'],
                forbid=params['forbid'],
                disable=params['disable'],
                menus=menus,
                roles=roles
            )

            s.add(item)
            data = copy.deepcopy(item.to_json())
            s.commit()
            return data
        except Exception as e:
            s.rollback()
            print(e)
            return str(e)

    def ModifyInterfaceRequest(self, interface_id, params):
        '''
        修改接口信息
        '''
        s = db.session()
        try:
            interface = s.query(Interface).filter(Interface.interface_id == interface_id).first()
            if not interface:
                return str('接口不存在')

            is_exists = self.isSaveExists(s, params, interface)

            if is_exists != True:
                return str(is_exists['error'])

            AllowableFields = ['name', 'path', 'method', 'description', 'disable']

            for i in params:
                if i in AllowableFields and hasattr(interface, i):
                    setattr(interface, i, params[i])

            menus = s.query(Menu).filter(Menu.menu_id.in_(params.getlist('menus[]'))).all()
            roles = s.query(Role).filter(Role.role_id.in_(params.getlist('roles[]'))).all()
            interface.menus = menus
            interface.roles = roles
            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

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
            print(e)
            s.rollback()
            return str(e)

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
            print(e)
            s.rollback()
            return str(e)
