#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限判断方法
@Author: Zpp
@Date: 2019-09-04 16:55:43
@LastEditTime: 2020-05-06 15:41:10
@LastEditors: Zpp
'''
from models import db
from models.system import Admin, Role, Interface, Menu, InitSql
from sqlalchemy import exists


def checkDb():
    s = db.session()
    try:
        res = s.query(InitSql).first()
        return res.isInit
    except Exception as e:
        return str('数据库未连接或者其他错误请查看错误信息：' + e.message)


def isExists(s, model, params):
    '''
    判断值是否已存在
    '''
    try:
        for i in params:
            querys = s.query(model).filter_by(**{
                i: params[i]['value']
            })

            is_exists = s.query(
                querys.exists()
            ).scalar()

            if is_exists:
                return {
                    'value': querys.one(),
                    'error': u'%s已存在' % params[i]['name']
                }

        return True
    except Exception as e:
        print e
        return True


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

        role = s.query(Role).filter(Role.role_id == admin.role_id, Role.is_disabled == False).one()
        if role:
            i = role.interfaces.filter(Interface.is_disabled == False, Interface.path == path).one()
            if i:
                return True
            m = role.menus.filter(Menu.is_disabled == False, Menu.path == path).one()
            if m:
                return True

        return False
    except Exception, e:
        print e
        return False
