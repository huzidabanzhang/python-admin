#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2019-09-09 10:02:39
@LastEditTime: 2019-10-15 09:59:58
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import User, Role, Route, Menu
from conf.setting import Config
from libs.error_code import RecordLog
import uuid
import datetime


class UserModel():
    def CreateDropRequest(self):
        try:
            db.drop_all()
            db.create_all()
            return True
        except Exception as e:
            print e
            return RecordLog(request.url, e)

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
