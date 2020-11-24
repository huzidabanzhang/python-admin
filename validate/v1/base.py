#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 数据库验证器
@Author: Zpp
@Date: 2020-05-28 13:44:29
@LastEditors: Zpp
@LastEditTime: 2020-05-28 14:02:02
'''

params = {
    # 验证字段
    'fields': {
        'type': {
            'name': '导出类型',
            'type': 'int',
            'between': [1, 2, 3],
            'required': True
        },
        'document': {
            'name': '数据库文件',
            'type': 'file',
            'required': True,
            'msg': '请选择上传数据库文件'
        },
        'admin_id': {
            'name': '管理员编号',
            'type': 'str',
            'required': True
        },
        'time': {
            'name': '查询时间',
            'type': 'str',
            'required': True
        }
    },
    # 导出数据库
    'Export': ['type'],
    # 导入数据库
    'Import': ['document'],
    # 首页登录清空
    'Login': ['admin_id', 'time']
}
