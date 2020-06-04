#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口验证器
@Author: Zpp
@Date: 2020-05-29 16:29:31
@LastEditors: Zpp
@LastEditTime: 2020-05-29 16:41:54
'''

params = {
    # 验证字段
    'fields': {
        'name': {
            'name': u'接口名称',
            'type': 'str',
            'required': True
        },
        'path': {
            'name': u'路径',
            'type': 'str',
            'required': True
        },
        'method': {
            'name': u'请求方式',
            'type': 'str',
            'between': ['GET', 'POST', 'PUT', 'DELETE'],
            'required': True
        },
        'mark': {
            'name': u'菜单标识',
            'type': 'str',
            'required': True
        },
        'description': {
            'name': u'描述',
            'type': 'str',
            'required': True
        },
        'menus[]': {
            'name': u'所属菜单',
            'type': 'list',
            'required': True
        },
        'forbid': {
            'name': u'可隐藏',
            'type': 'boolean',
            'required': True
        },
        'disable': {
            'name': u'可见性',
            'type': 'boolean',
            'required': True
        },
        'interface_id[]': {
            'name': u'接口编号',
            'type': 'list',
            'required': True
        },
        'interface_id': {
            'name': u'接口编号',
            'type': 'str',
            'required': True
        },
        'page': {
            'name': u'页码',
            'type': 'int',
            'default': 1
        },
        'page_size': {
            'name': u'条数',
            'type': 'int',
            'default': 20
        },
        'order_by': {
            'name': u'排序字段',
            'type': 'str',
            'default': None
        }
    },
    'Create': ['name', 'path', 'method', 'description', 'menus[]', 'mark', 'forbid', 'disable'],
    'Modify': ['interface_id', 'name', 'path', 'method', 'description', 'menus[]', 'mark', 'forbid', 'disable'],
    'Del': ['interface_id[]'],
    'Lock': ['interface_id[]', 'disable'],
    'Query': [{
        'field': 'disable',
        'required': False
    }, {
        'field': 'name',
        'required': False
    }, {
        'field': 'method',
        'required': False
    }, 'page', 'page_size', 'order_by']
}
