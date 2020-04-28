#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:05:51
@LastEditTime: 2020-04-28 14:19:08
@LastEditors: Zpp
'''
from flask import request
from models import db
from models.system import Menu, Role
from conf.setting import default
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
                    if role.mark == default['role_mark']:
                        for i in menus:
                            select.append(i['menu_id'])
                    else:
                        for value in role.interfaces:
                            select.append(value.interface_id)
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
                cache=params['cache']
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

            AllowableFields = ['pid', 'title', 'path', 'icon', 'sort', 'component', 'componentPath', 'name', 'cache']
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

    def LockMenuRequest(self, menu_id, is_disabled):
        '''
        禁用菜单
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.menu_id == menu_id).first()

            if not is_disabled:
                parent = s.query(Menu).filter(Menu.menu_id == menu.pid, Menu.is_disabled == True).first()
                if parent:
                    return str('父菜单处于禁用状态, 该菜单不能启用')

            menu.is_disabled = is_disabled
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
