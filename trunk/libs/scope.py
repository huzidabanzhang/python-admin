#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 16:55:43
@LastEditTime: 2019-10-15 10:20:19
@LastEditors: Zpp
'''
from models.base import db
from models.system import User, Role, Route


def is_in_scope(user_id, endpoint):
    '''
    路由权限判断
    '''
    s = db.session()
    try:
        user = s.query(User).filter(User.user_id == user_id).first()
        if not user:
            return str('用户不存在')
        if not user.isLock:
            return str('用户被禁用')

        role = s.query(Role).filter(Role.id == user.role_id).first()
        route = []
        if role:
            for i in role.routes:
                route.append(i.to_json())
        print endpoint
        if not route:
            return False

        return True
    except Exception, e:
        print e
        return False
