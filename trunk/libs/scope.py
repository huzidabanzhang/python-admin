#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限判断方法
@Author: Zpp
@Date: 2019-09-04 16:55:43
@LastEditTime: 2020-02-21 16:45:05
@LastEditors: Please set LastEditors
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


        role = s.query(Role).filter(Role.id == admin.role_id, Role.is_disabled == False).first()
        if role:
            i = role.interfaces.filter(Interface.is_disabled == False, Interface.path == path)
            if i:
                return True
            m = role.menus.filter(Menu.is_disabled == False, Menu.path == path)
            if m:
                return True
            r = s.query(Route).filter(RoRoutele.path == path, Route.is_disabled == False).first()
            if r:
                return True

        return False
    except Exception, e:
        print e
        return False
