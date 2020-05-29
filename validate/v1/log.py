#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志验证器
@Author: Zpp
@Date: 2020-05-29 14:00:21
@LastEditors: Zpp
@LastEditTime: 2020-05-29 14:32:18
'''

params = {
    # 验证字段
    'fields': {
        'type[]': {
            'name': u'日志类型',
            'type': 'list'
        },
        'status[]': {
            'name': u'日志状态',
            'type': 'list'
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
        }
    },
    'Query': ['type[]', 'status[]', 'page', 'page_size']
}
