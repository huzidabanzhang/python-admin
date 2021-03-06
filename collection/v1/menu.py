#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:05:51
LastEditTime: 2020-12-01 13:59:26
LastEditors: Zpp
'''
from flask import request
from models import db
from models.system import Menu, Role
from conf.setting import default
from libs.scope import isExists
from sqlalchemy import text
import uuid
import json


class MenuModel():
    def __init__(self):
        self.exists = {
            'name': '路由名称',
            'title': '菜单名称',
            'path': '路由',
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

        return isExists(s, Menu, d)

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

        return isExists(s, Menu, d)

    def QueryMenuByParamRequest(self, params, is_interface=False):
        '''
        菜单列表
        '''
        s = db.session()
        try:
            data = {}
            if 'disable' in params:
                data['disable'] = params['disable']

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
                            'menu_id': '%s.%s' % (value.menu_id, item.interface_id)
                        })
                    menus.append({
                        'type': 'MENU',
                        'title': value.title,
                        'menu_id': value.menu_id,
                        'pid': value.pid,
                        'children': interfaces,
                        'count': Menu.query.filter(Menu.pid == value.menu_id).count()
                    })

                if 'role_id' in params:
                    role = Role.query.filter(Role.role_id == params['role_id']).first()

                    # vue树形控件的选择原理 只需要子节点id
                    for i in role.interfaces:
                        for m in i.menus:
                            select.append('%s.%s' % (m.menu_id, i.interface_id))
                    # 补充没有接口的菜单
                    menu = [i.menu_id for i in role.menus]
                    for i in menus:
                        if len(i['children']) == 0 and i['count'] == 0 and i['menu_id'] in menu:
                            select.append(i['menu_id'])

                return {
                    'data': menus,
                    'select': select
                }
            else:
                res = []
                for i in result:
                    roles = [r.role_id for r in i.roles]
                    item = i.to_json()
                    item['roles'] = roles
                    res.append(item)

                return res
        except Exception as e:
            print(e)
            return str(e)

    def CreateMenuRequest(self, params):
        '''
        新建菜单
        '''
        s = db.session()
        is_exists = self.isCreateExists(s, params)

        if is_exists != True:
            return str(is_exists['error'])

        try:
            menu = Menu(
                menu_id=str(uuid.uuid4()),
                pid=params['pid'],
                title=params['title'],
                sort=int(params['sort']),
                path=params['path'],
                mark=params['mark'],
                icon=params['icon'],
                component=params['component'],
                componentPath=params['componentPath'],
                name=params['name'],
                cache=params['cache'],
                disable=params['disable']
            )

            # 角色关联
            res = s.query(Role).filter(Role.role_id.in_(params.getlist('roles[]'))).all()
            menu.roles = res
            s.add(menu)

            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print(e)
            return str(e)

    def ModifyMenuRequest(self, menu_id, params):
        '''
        修改菜单信息
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            if not menu:
                return str('菜单不存在')

            is_exists = self.isSaveExists(s, params, menu)

            if is_exists != True:
                return str(is_exists['error'])

            AllowableFields = ['pid', 'title', 'path', 'icon', 'sort', 'component', 'componentPath', 'name', 'cache', 'disable']

            for i in params:
                if i in AllowableFields and hasattr(menu, i):
                    setattr(menu, i, params[i])

            # 角色关联
            res = s.query(Role).filter(Role.role_id.in_(params.getlist('roles[]'))).all()
            menu.roles = res

            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

    def DelMenuRequest(self, menu_id):
        '''
        删除菜单
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            s.delete(menu)

            # 子菜单移动到根目录
            s.query(Menu).filter(Menu.pid == menu_id).update({
                'pid': '0'
            })
            s.commit()
            return True
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)

    def GetMenuToInterfaceRequest(self, menu_id):
        '''
        获取菜单下级联的API接口
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            return [i.to_json() for i in menu.interfaces]
        except Exception as e:
            print(e)
            s.rollback()
            return str(e)
