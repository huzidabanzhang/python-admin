#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限判断方法
@Author: Zpp
@Date: 2019-09-04 16:55:43
@LastEditTime: 2019-11-25 10:51:26
@LastEditors: Zpp
'''
from models.base import db
from models.system import Admin, Role, Route, Interface, Menu


def is_in_scope(admin_id, path):
    '''
    路由权限判断
    '''
    s = db.session()
    try:
        admin = s.query(Admin).filter(Admin.admin_id == admin_id).first()
        if not admin:
            return str('管理员不存在')
        if not admin.isLock:
            return str('管理员被禁用')


        role = s.query(Role).filter(Role.id == admin.role_id, Role.isLock == True).first()
        if role:
            route = role.routes.filter(Route.isLock == True, Route.path == path)
            if route:
                return True
            else:
                interface = role.menus.join(Interface).filter(Menu.isLock == True, Interface.path == path)
                if interface:
                    return True

        return False
    except Exception, e:
        print e
        return False
