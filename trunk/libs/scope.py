#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限判断方法
@Author: Zpp
@Date: 2019-09-04 16:55:43
@LastEditTime: 2020-05-06 10:02:51
@LastEditors: Zpp
'''
from models import db
from models.system import Admin, Role, Interface, Menu, InitSql


def checkDb():
    try:
        s = db.session()
        res = s.query(InitSql).first()
        return res.isInit
    except Exception as e:
        return str('数据库未连接或者其他错误请查看错误信息：' + e.message)


def is_in_scope(admin_id, path):
    '''
    路由权限判断
    '''
    s = db.session()
    try:
        admin = s.query(Admin).filter(Admin.admin_id == admin_id).first()
        if not admin:
            return str('管理员不存在')
        if admin.is_disabled:
            return str('管理员被禁用')


        role = s.query(Role).filter(Role.role_id == admin.role_id, Role.is_disabled == False).first()
        if role:
            i = role.interfaces.filter(Interface.is_disabled == False, Interface.path == path)
            if i:
                return True
            m = role.menus.filter(Menu.is_disabled == False, Menu.path == path)
            if m:
                return True

        return False
    except Exception, e:
        print e
        return False
