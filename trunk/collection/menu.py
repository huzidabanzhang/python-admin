#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:05:51
@LastEditTime : 2020-02-12 20:03:49
@LastEditors  : Please set LastEditors
'''
from flask import request
from models.base import db
from models.system import Menu, Role
from sqlalchemy import text
import uuid


class MenuModel():
    def QueryMenuByParamRequest(self, params, is_interface=False):
        '''
        菜单列表
        '''
        s = db.session()
        try:
            data = {}
            if params.has_key('is_disabled'):
                data['is_disabled'] = params['is_disabled']

            result = Menu.query.filter_by(**data).order_by(Menu.sort, Menu.id).all()

            if is_interface:
                select = []
                menus = []
                for value in result:
                    interfaces = []
                    for item in value.interfaces:
                        interfaces.append({
                            'type': 'INTERFACE',
                            'title': item.description,
                            'menu_id': item.interface_id
                        })
                    menus.append({
                        'type': 'MENU',
                        'title': value.title,
                        'menu_id': value.menu_id,
                        'pid': value.pid,
                        'children': interfaces
                    })
                
                if params.has_key('role_id'):
                    role = Role.query.filter(Role.role_id == params['role_id']).first()
                    result = role.menus.filter(Menu.is_disabled == params['is_disabled'])
                    for value in result:
                        for item in value.interfaces:
                            select.append(item.interface_id)

                return {
                    'data': menus,
                    'select': select
                }
            else:
                return [value.to_json() for value in result]
        except Exception as e:
            print e
            return str(e.message)

    def CreateMenuRequest(self, params):
        '''
        新建菜单
        '''
        s = db.session()
        try:
            item = Menu(
                menu_id=uuid.uuid4(),
                parent_id=params['parent_id'],
                title=params['title'],
                type=int(params['type']),
                sort=int(params['sort']),
                path=params['path'],
                icon=params['icon']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetMenuRequest(self, menu_id):
        '''
        查询菜单
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            if not menu:
                return str('菜单不存在')

            return menu.to_json()
        except Exception as e:
            print e
            return str(e.message)

    def ModifyMenuRequest(self, menu_id, params):
        '''
        修改菜单信息
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            if not menu:
                return str('菜单不存在')

            AllowableFields = ['parent_id', 'title', 'path', 'icon', 'sort', 'type']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Menu).filter(Menu.menu_id == menu_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockMenuRequest(self, menu_id, isLock):
        '''
        禁用菜单
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()

            if isLock:
                parent = s.query(Menu).filter(Menu.menu_id == menu.parent_id, Menu.isLock == False).first()
                if parent:
                    return str('父菜单处于禁用状态, 该菜单不能启用')

            menu.isLock = isLock
            s.commit()

            if not isLock:
                s.query(Menu).filter(Menu.parent_id == menu_id, Menu.isLock == True).update({Menu.isLock: False})
                s.commit()

            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
