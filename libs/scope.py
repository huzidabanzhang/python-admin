#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 鉴权判断方法
@Author: Zpp
@Date: 2019-09-04 16:55:43
LastEditTime: 2020-12-01 13:39:07
LastEditors: Zpp
'''
from models import db
from models.system import Admin, Role, Interface, Menu, InitSql
from sqlalchemy import exists
import json


def checkDb():
    s = db.session()
    try:
        res = s.query(InitSql).first()
        return res.is_init
    except Exception as e:
        return str('数据库未连接或者其他错误请查看错误信息：%s' % e)


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
                    'error': '%s已存在' % params[i]['name']
                }

        return True
    except Exception as e:
        print(e)
        return True


def is_in_scope(admin_id, path):
    '''
    路由鉴权判断
    '''
    s = db.session()
    try:
        admin = s.query(Admin).filter(Admin.admin_id == admin_id).first()
        if not admin:
            return str('管理员不存在')
        if admin.disable:
            return str('管理员被禁用')

        role = s.query(Role).filter(Role.role_id == admin.role_id, Role.disable == False).one()
        if role:
            interface = role.interfaces.filter(Interface.disable == False, Interface.path == path)
            if interface:
                return True

            menu = role.menus.filter(Menu.disable == False, Menu.path == path)
            if menu:
                return True

        return False
    except Exception as e:
        print(e)
        return False
