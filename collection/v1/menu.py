#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:05:51
@LastEditTime: 2020-05-06 17:29:52
@LastEditors: Zpp
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
            'name': u'路由名称',
            'title': u'菜单名称',
            'path': u'路由',
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

        return isExists(s, Menu, d)

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

        return isExists(s, Menu, d)

    def QueryMenuByParamRequest(self, params, is_interface=False):
        '''
        菜单列表
        '''
        s = db.session()
        try:
            data = {}
            if params.has_key('disable'):
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
                        'children': interfaces
                    })

                if params.has_key('role_id'):
                    role = Role.query.filter(Role.role_id == params['role_id']).first()
                    if role.mark == default['role_mark']:
                        for i in menus:
                            select.append(i['menu_id'])
                    else:
                        for value in json.loads(role.role_list)['I']:
                            select.append(value)
                        # for value in role.menus:
                        #     select.append(value.menu_id)

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
        is_exists = self.isCreateExists(s, params)

        if is_exists != True:
            return str(is_exists['error'].encode('utf8'))

        try:
            item = Menu(
                menu_id=uuid.uuid4(),
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
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
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

            AllowableFields = ['pid', 'title', 'path', 'icon', 'sort', 'component', 'componentPath', 'name', 'cache', 'disable']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            is_exists = self.isSaveExists(s, data, menu)

            if is_exists != True:
                return str(is_exists['error'].encode('utf8'))

            s.query(Menu).filter(Menu.menu_id == menu_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

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
            print e
            s.rollback()
            return str(e.message)

    def GetMenuToInterfaceRequest(self, menu_id):
        '''
        获取菜单下级联的API接口
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()
            return [i.to_json() for i in menu.interfaces]
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
