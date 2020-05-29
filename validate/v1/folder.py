#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹验证器
@Author: Zpp
@Date: 2020-05-29 11:28:26
@LastEditors: Zpp
@LastEditTime: 2020-05-29 14:40:01
'''

params = {
    # 验证字段
    'fields': {
        'name': {
            'name': u'文件夹名称',
            'type': 'str',
            'required': True
        },
        'admin_id': {
            'name': u'管理员编号',
            'type': 'str',
            'required': True
        },
        'pid': {
            'name': u'父编号',
            'type': 'str',
            'required': True,
            'default': '0'
        },
        'is_sys': {
            'name': u'是否是系统文件夹',
            'type': 'boolean',
            'required': True
        },
        'folder_id': {
            'name': u'所属文件夹',
            'type': 'str',
            'required': True
        }
    },
    'Create': ['admin_id', 'name', 'pid', 'is_sys'],
    'Modify': ['folder_id', 'name', {
        'field': 'pid',
        'required': False
    }],
    'Query': ['pid', 'admin_id'],
    'Del': ['folder_id']
}
