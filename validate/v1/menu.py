#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 菜单验证器
@Author: Zpp
@Date: 2020-05-29 14:08:17
@LastEditors: Zpp
@LastEditTime: 2020-05-29 14:56:01
'''

params = {
    # 验证字段
    'fields': {
        'pid': {
            'name': '父编号',
            'type': 'str',
            'required': True,
            'default': '0'
        },
        'title': {
            'name': '菜单名称',
            'type': 'str',
            'required': True
        },
        'name': {
            'name': '路由名称',
            'type': 'str',
            'required': True
        },
        'path': {
            'name': '路径',
            'type': 'str',
            'required': True
        },
        'icon': {
            'name': '菜单图标',
            'type': 'str',
            'required': True
        },
        'mark': {
            'name': '菜单标识',
            'type': 'str',
            'required': True
        },
        'sort': {
            'name': '排序',
            'type': 'int',
            'required': True
        },
        'component': {
            'name': '路由组件',
            'type': 'str',
            'required': True
        },
        'componentPath': {
            'name': '组件路径',
            'type': 'str',
            'required': True
        },
        'disable': {
            'name': '可见性',
            'type': 'boolean',
            'required': True
        },
        'cache': {
            'name': '路由缓存',
            'type': 'boolean',
            'required': True
        },
        'menu_id': {
            'name': '菜单编号',
            'type': 'str',
            'required': True
        },
        'role_id': {
            'name': '角色',
            'type': 'str',
            'required': True
        },
        'is_interface': {
            'name': '是否带API',
            'type': 'boolean'
        }
    },
    'Create': ['pid', 'title', 'path', 'icon', 'mark', 'sort', 'component', 'componentPath', 'name', 'cache', 'disable'],
    'Get': ['menu_id'],
    'Modify': ['menu_id', 'pid', 'title', 'path', 'icon', 'mark', 'sort', 'component', 'componentPath', 'name', 'cache', 'disable'],
    'Del': ['menu_id'],
    'Query': ['is_interface', {
        'field': 'disable',
        'required': False
    }, {
        'field': 'role_id',
        'required': False
    }]
}
