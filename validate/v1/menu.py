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
            'name': u'父编号',
            'type': 'str',
            'required': True,
            'default': '0'
        },
        'title': {
            'name': u'菜单名称',
            'type': 'str',
            'required': True
        },
        'name': {
            'name': u'路由名称',
            'type': 'str',
            'required': True
        },
        'path': {
            'name': u'路径',
            'type': 'str',
            'required': True
        },
        'icon': {
            'name': u'菜单图标',
            'type': 'str',
            'required': True
        },
        'mark': {
            'name': u'菜单标识',
            'type': 'str',
            'required': True
        },
        'sort': {
            'name': u'排序',
            'type': 'int',
            'required': True
        },
        'component': {
            'name': u'路由组件',
            'type': 'str',
            'required': True
        },
        'componentPath': {
            'name': u'组件路径',
            'type': 'str',
            'required': True
        },
        'is_disabled': {
            'name': u'可见性',
            'type': 'boolean',
            'required': True
        },
        'cache': {
            'name': u'路由缓存',
            'type': 'boolean',
            'required': True
        },
        'menu_id': {
            'name': u'菜单编号',
            'type': 'str',
            'required': True
        },
        'role_id': {
            'name': u'角色',
            'type': 'str',
            'required': True
        },
        'is_interface': {
            'name': u'是否带API',
            'type': 'boolean'
        }
    },
    'Create': ['pid', 'title', 'path', 'icon', 'mark', 'sort', 'component', 'componentPath', 'name', 'cache', 'is_disabled'],
    'Get': ['menu_id'],
    'Modify': ['menu_id', 'pid', 'title', 'path', 'icon', 'mark', 'sort', 'component', 'componentPath', 'name', 'cache', 'is_disabled'],
    'Del': ['menu_id'],
    'Query': ['is_interface', {
        'field': 'is_disabled',
        'required': False
    }, {
        'field': 'role_id',
        'required': False
    }]
}
