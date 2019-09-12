#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-09 10:02:39
@LastEditTime: 2019-09-12 11:26:16
@LastEditors: Zpp
'''
from models.base import db
from models.user import User
from conf.setting import Config
import uuid
import datetime


class UserModel():
    def CreateDropRequest(self):
        db.drop_all()
        db.create_all()
        return True

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
            return str(e.message)
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
                nickname=params['nickname']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)
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

            return user.to_json()
        except Exception as e:
            print e
            return str(e.message)
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

            AllowableFields = ['password', 'nickname', 'sex', 'role_id']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]
            data['update_time'] = datetime.datetime.now
            s.query(User).filter(User.user_id == user_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
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
            return str(e.message)
        finally:
            s.close()
