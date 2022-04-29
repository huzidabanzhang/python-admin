#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 管理员验证器
@Author: Zpp
@Date: 2020-05-27 16:56:52
LastEditors: Zpp
LastEditTime: 2022-03-22 08:55:38
'''

params = {
    # 验证字段
    'fields': {
        'code': {
            'name': '验证码',
            'type': 'str',
            'min': 4,
            'max': 4,
            'required': True
        },
        'username': {
            'name': '用户名',
            'type': 'str',
            'min': 2,
            'required': True
        },
        'password': {
            'name': '密码',
            'type': 'str',
            'min': 6,
            'required': True
        },
        'nickname': {
            'name': '昵称',
            'type': 'str',
            'default': ''
        },
        'email': {
            'name': '邮件',
            'type': 'email',
            'default': ''
        },
        'sex': {
            'name': '性别',
            'type': 'int',
            'default': 1
        },
        'role_id': {
            'name': '角色',
            'type': 'str',
            'required': True
        },
        'disable': {
            'name': '可见性',
            'type': 'boolean',
            'required': True
        },
        'avatar': {
            'name': '头像',
            'type': 'str',
            'default': ''
        },
        'admin_id': {
            'name': '管理员编号',
            'type': 'str',
            'required': True
        },
        'admin_id[]': {
            'name': '管理员编号',
            'type': 'list',
            'required': True
        },
        'page': {
            'name': '页码',
            'type': 'int',
            'default': 1
        },
        'page_size': {
            'name': '条数',
            'type': 'int',
            'default': 20
        },
        'order_by': {
            'name': '排序字段',
            'type': 'str',
            'default': None
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
    'Del': ['admin_id[]'],
    'Query': [{
        'field': 'disable',
        'required': False
    }, {
        'field': 'role_id',
        'required': False
    }, 'page', 'page_size', 'order_by']
}
