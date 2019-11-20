#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2019-09-09 10:02:39
@LastEditTime: 2019-11-20 14:25:22
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import Admin, Role, Route, Menu, Interface
from conf.setting import Config, init_route, init_menu
from sqlalchemy import text
import uuid
import datetime


class AdminModel():
    def CreateDropRequest(self):
        try:
            db.drop_all()
            db.create_all()

            s = db.session()
            admin = Admin(
                admin_id=uuid.uuid4(),
                username=u'Admin',
                password=Config().get_md5('123456'),
                avatarUrl='',
                role_id=1
            )
            s.add(admin)
            s.commit()

            role_id = uuid.uuid4()
            role = Role(role_id=role_id, name=u'超级管理员', checkKey='[]')
            s.add(role)
            s.commit()

            self.__init_routes(init_route, '0', role_id)
            self.__init_menus(init_menu, '0', role_id)
            return True
        except Exception as e:
            print e
            return str(e.message)

    def __init_routes(self, data, parentId, role_id):
        s = db.session()
        for r in data:
            route_id = uuid.uuid4()
            route = self.__create_route(r, route_id, parentId)
            s.add(route)

            role = s.query(Role).filter(Role.role_id == role_id).first()
            routes = []
            for i in role.routes:
                routes.append(i)
            routes.append(route)
            role.routes = routes

            s.commit()
            if r.has_key('children'):
                self.__init_routes(r['children'], route_id, role_id)

    def __init_menus(self, data, parentId, role_id):
        s = db.session()
        for m in data:
            menu_id = uuid.uuid4()
            menu = self.__create_menu(m, menu_id, parentId)

            if m.has_key('interface'):
                interfaces = []
                for f in m['interface']:
                    interface = self.__create_interface(f, uuid.uuid4(), menu_id)
                    s.add(interface)
                    s.commit()
                    interfaces.append(interface)
                menu.interfaces = interfaces
            s.add(menu)

            role = s.query(Role).filter(Role.role_id == role_id).first()
            menus = []
            for i in role.menus:
                menus.append(i)
            menus.append(menu)
            role.menus = menus

            s.commit()
            if m.has_key('children'):
                self.__init_menus(m['children'], menu_id, role_id)

    def __create_route(self, params, route_id, parentId):
        return Route(
            route_id=route_id,
            parentId=parentId,
            name=params['name'],
            title=params['title'],
            path=params['path'],
            component=params['component'],
            componentPath=params['componentPath'],
            cache=params['cache']
        )

    def __create_menu(self, params, menu_id, parentId):
        return Menu(
            menu_id=menu_id,
            parentId=parentId,
            title=params['title'],
            path=params['path'],
            icon=params['icon']
        )

    def __create_interface(self, params, interface_id, menu_id):
        return Interface(
            menu_id=menu_id,
            interface_id=interface_id,
            name=params['name'],
            path=params['path'],
            method=params['method'],
            description=params['description']
        )

    def QueryAdminByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        管理员列表
        '''
        s = db.session()
        try:
            data = {}
            for i in ['role_id', 'isLock']:
                if params.has_key(i):
                    data[i] = params[i]

            result = Admin.query.filter_by(**data).order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)

    def CreateAdminRequest(self, params):
        '''
        新建管理员
        '''
        s = db.session()
        try:
            if params['role_id'] == 1:
                return str('不能设为为超级管理员')

            admin = s.query(Admin).filter(Admin.username == params['username']).first()

            if admin:
                return str('管理员已存在')

            item = Admin(
                admin_id=uuid.uuid4(),
                username=params['username'],
                password=Config().get_md5(params['password']),
                sex=int(params['sex']),
                nickname=params['nickname'],
                role_id=int(params['role_id']),
                avatarUrl=params['avatarUrl']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetAdminRequest(self, username, password):
        '''
        查询管理员
        '''
        s = db.session()
        try:
            admin = s.query(Admin).filter(Admin.username == username, Admin.password == Config().get_md5(password)).first()
            if not admin:
                return str('管理员不存在')
            if not admin.isLock:
                return str('管理员被禁用')

            data = admin.to_json()
            route = []
            menu = []
            interface = []
            role = s.query(Role).filter(Role.id == admin.role_id).first()
            if role:
                for i in role.routes:
                    item = i.to_json()
                    if item['isLock']:
                        route.append(item)

                for i in role.menus.filter(Menu.isLock == True).order_by(Menu.sort, Menu.id):
                    menu.append(i.to_json())
                    interfaces = s.query(Interface).filter(Interface.menu_id == i.menu_id, Interface.isLock == True).all()
                    interface = interface + [i.to_json() for i in interfaces]

            data['routes'] = route
            data['menus'] = menu
            data['interface'] = interface
            return data
        except Exception as e:
            print e
            return str(e.message)

    def ModifyAdminRequest(self, admin_id, params):
        '''
        修改管理员信息
        '''
        s = db.session()
        try:
            if params['role_id'] == 1:
                return str('不能设为为超级管理员')

            admin = s.query(Admin).filter(Admin.admin_id == admin_id).first()
            if not admin:
                return str('管理员不存在')
            if not admin.isLock:
                return str('管理员被禁用')

            AllowableFields = ['nickname', 'sex', 'role_id', 'avatarUrl', 'password']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    if i == 'password':
                        if params[i] != admin.password:
                            data[i] = Config().get_md5(params[i])
                    else:
                        data[i] = params[i]

            s.query(Admin).filter(Admin.admin_id == admin_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockAdminRequest(self, admin_id, isLock):
        '''
        禁用管理员
        '''
        s = db.session()
        try:
            for key in admin_id:
                admin = s.query(Admin).filter(Admin.admin_id == key).first()
                if not admin:
                    continue
                admin.isLock = isLock
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
