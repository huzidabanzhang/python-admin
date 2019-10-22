#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限控制器
@Author: Zpp
@Date: 2019-09-10 16:01:46
@LastEditTime: 2019-10-22 15:48:21
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import Role, Route, Menu
from sqlalchemy import text
import uuid


class RoleModel():
    def CreateRoleRequest(self, params):
        '''
        新建权限
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id.in_(route_id)).all()
            menu = s.query(Menu).filter(Menu.menu_id.in_(menu_id)).all()

            item = Role(
                name=params['name'],
                role_id=uuid.uuid4,
                routes=route,
                menus=menu
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

    def ModifyRoleToRoute(self, role_id, route_id):
        '''
        修改路由权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            route = s.query(Route).filter(Route.route_id.in_(route_id)).all()
            role.routes = route
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def ModifyRoleToMenu(self, role_id, menu_id):
        '''
        修改菜单权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            menu = s.query(Menu).filter(Menu.menu_id.in_(menu_id)).all()
            role.menus = menu
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def ModifyRoleRequest(self, role_id, name):
        '''
        修改权限信息
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            role.name = name
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockRoleRequest(self, role_id):
        '''
        禁用权限
        '''
        s = db.session()
        try:
            for key in role_id:
                role = s.query(Role).filter(Role.role_id == key).first()
                if not role:
                    continue
                role.isLock = False
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
            if params.has_key('isLock'):
                data['isLock'] = params['isLock']

            result = Role.query.filter_by(**data).order_by(text('id')).all()

            data = []
            for value in result:
                data.append(value.to_json())

            return data
        except Exception as e:
            print e
            return str(e.message)
