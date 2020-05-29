#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 角色验证器
@Author: Zpp
@Date: 2020-05-29 14:21:43
@LastEditors: Zpp
@LastEditTime: 2020-05-29 14:27:32
'''

params = {
    # 验证字段
    'fields': {
        'name': {
            'name': u'角色名称',
            'type': 'str',
            'required': True
        },
        'mark': {
            'name': u'角色标识',
            'type': 'str',
            'required': True
        },
        'is_disabled': {
            'name': u'可见性',
            'type': 'boolean',
            'required': True
        },
        'role_list[]': {
            'name': u'API列表',
            'type': 'list',
            'required': True
        },
        'menu[]': {
            'name': u'菜单列表',
            'type': 'list',
            'required': True
        },
        'role_id[]': {
            'name': u'角色编号',
            'type': 'list',
            'required': True
        },
        'role_id': {
            'name': u'角色编号',
            'type': 'str',
            'required': True
        }
    },
    'Create': ['name', 'mark', 'role_list[]', 'is_disabled', 'menu[]'],
    'Modify': ['role_id', 'name', 'mark', 'role_list[]', 'is_disabled', 'menu[]'],
    'Lock': ['role_id[]', 'is_disabled'],
    'Del': ['role_id[]'],
    'Query': [{
        'field': 'is_disabled',
        'required': False
    }]
}
