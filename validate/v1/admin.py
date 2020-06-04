#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 管理员验证器
@Author: Zpp
@Date: 2020-05-27 16:56:52
@LastEditors: Zpp
@LastEditTime: 2020-05-28 11:10:19
'''

params = {
    # 验证字段
    'fields': {
        'code': {
            'name': u'验证码',
            'type': 'str',
            'min': 4,
            'max': 4,
            'required': True
        },
        'username': {
            'name': u'用户名',
            'type': 'str',
            'min': 6,
            'required': True
        },
        'password': {
            'name': u'密码',
            'type': 'str',
            'min': 6,
            'required': True
        },
        'nickname': {
            'name': u'昵称',
            'type': 'str',
            'default': ''
        },
        'email': {
            'name': u'邮件',
            'type': 'email',
            'default': ''
        },
        'sex': {
            'name': u'性别',
            'type': 'int',
            'default': 1
        },
        'role_id': {
            'name': u'角色',
            'type': 'str',
            'required': True
        },
        'disable': {
            'name': u'可见性',
            'type': 'boolean',
            'required': True
        },
        'avatar': {
            'name': u'头像',
            'type': 'str',
            'default': ''
        },
        'admin_id': {
            'name': u'管理员编号',
            'type': 'str',
            'required': True
        },
        'admin_id[]': {
            'name': u'管理员编号',
            'type': 'list',
            'required': True
        }
    },
    # 登录验证
    'Login': ['code', 'username', 'password'],
    # 创建管理员
    'Create': ['username', 'password', 'nickname', 'email', 'sex', 'role_id', 'disable', 'avatar'],
    # 编辑管理员
    'Modify': ['admin_id', 'password', 'nickname', 'email', 'sex', 'role_id', 'disable', 'avatar'],
    # 禁用管理员
    'Lock': ['admin_id[]', 'disable'],
    # 删除管理员
    'Del': ['admin_id[]']
}
