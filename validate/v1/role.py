#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 角色验证器
@Author: Zpp
@Date: 2020-05-29 14:21:43
LastEditors: Zpp
LastEditTime: 2020-11-26 11:09:27
'''

params = {
    # 验证字段
    'fields': {
        'name': {
            'name': '角色名称',
            'type': 'str',
            'required': True
        },
        'mark': {
            'name': '角色标识',
            'type': 'str',
            'required': True
        },
        'disable': {
            'name': '可见性',
            'type': 'boolean',
            'required': True
        },
        'interface[]': {
            'name': 'API列表',
            'type': 'list',
            'required': True
        },
        'menu[]': {
            'name': '菜单列表',
            'type': 'list',
            'required': True
        },
        'role_id[]': {
            'name': '角色编号',
            'type': 'list',
            'required': True
        },
        'role_id': {
            'name': '角色编号',
            'type': 'str',
            'required': True
        },
        'is_default': {
            'name': '获取系统角色Id',
            'type': 'boolean'
        }
    },
    'Create': ['name', 'mark', 'interface[]', 'disable', 'menu[]'],
    'Modify': ['role_id', 'name', 'mark', 'interface[]', 'disable', 'menu[]'],
    'Lock': ['role_id[]', 'disable'],
    'Del': ['role_id[]'],
    'Query': [{
        'field': 'disable',
        'required': False
    }, 'is_default']
}
