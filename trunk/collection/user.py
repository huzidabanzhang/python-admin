#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2019-09-09 10:02:39
@LastEditTime: 2019-10-15 15:37:47
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import User, Role, Route, Menu, Interface
from conf.setting import Config, init_route, init_menu
from libs.error_code import RecordLog
import uuid
import datetime


class UserModel():
    def CreateDropRequest(self):
        try:
            db.drop_all()
            db.create_all()

            s = db.session()
            admin = User(
                user_id=uuid.uuid4(),
                username=u'Admin',
                password=Config().get_md5('123456'),
                avatarUrl='',
                role_id=1
            )
            s.add(admin)
            s.commit()

            role = Role(role_id=uuid.uuid4(), name=u'超级管理员')
            s.add(role)
            s.commit()

            self.__init_routes(init_route, '0')
            self.__init_menus(init_menu, '0')
            return True
        except Exception as e:
            print e
            return RecordLog(request.url, e)
    
    def __init_routes(self, data, parentId):
        s = db.session()
        for r in data:
            route_id = uuid.uuid4()
            route = self.__create_route(r, route_id, parentId)
            s.add(route)
            s.commit()
            if r.has_key('children'):
                return self.__init_routes(r['children'], route_id)

    def __init_menus(self, data, parentId):
        s = db.session()
        for m in data:
            menu_id = uuid.uuid4()
            menu = self.__create_menu(m, menu_id, parentId)
            s.add(menu)
            s.commit()
            if m.has_key('interface'):
                for f in m['interface']:
                    interface = self.__create_interface(f, uuid.uuid4(), menu_id)
                    s.add(interface)
                    s.commit()
            if m.has_key('children'):
                return self.__init_menus(m['children'], menu_id)

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

    def QueryUserByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        用户列表
        '''
        s = db.session()
        try:
            Int = ['sex', 'role_id', 'isLock']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = User.query.filter_by(*data).filter(
                User.username.like("%" + params['username'] + "%") if params.has_key('username') else '',
                User.nickname.like("%" + params['nickname'] + "%") if params.has_key('nickname') else ''
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def CreateUserRequest(self, params):
        '''
        新建用户
        '''
        s = db.session()
        try:
            user = s.query(User).filter(User.username == params['username']).first()

            if user:
                return str('用户已存在')

            item = User(
                user_id=uuid.uuid4(),
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
            return RecordLog(request.url, e)
        finally:
            s.close()

    def GetUserRequest(self, username, password):
        '''
        查询用户
        '''
        s = db.session()
        try:
            user = s.query(User).filter(User.username == username, User.password == Config().get_md5(password)).first()
            if not user:
                return str('用户不存在')
            if not user.isLock:
                return str('用户被禁用')

            data = user.to_json()
            route = []
            menu = []
            interface = []
            role = s.query(Role).filter(Role.id == user.role_id).first()
            if role:
                for i in role.routes:
                    route.append(i.to_json())
                for i in role.menus:
                    menu.append(i.to_json())
                    for j in i.interfaces:
                        interface.append(j.to_json())

            data['routes'] = route
            data['menus'] = menu
            data['interface'] = interface

            return data
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def ModifyUserRequest(self, user_id, params):
        '''
        修改用户信息
        '''
        s = db.session()
        try:
            user = s.query(User).filter(User.user_id == user_id).first()
            if not user:
                return str('用户不存在')
            if not user.isLock:
                return str('用户被禁用')
            if params['role_id'] == 1:
                return str('不能设为为超级管理员')

            AllowableFields = ['password', 'nickname', 'sex', 'role_id', 'avatarUrl']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(User).filter(User.user_id == user_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()

    def LockUserRequest(self, user_id):
        '''
        禁用用户
        '''
        s = db.session()
        try:
            for key in user_id:
                user = s.query(User).filter(User.user_id == key).first()
                if not user:
                    continue
                user.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()
