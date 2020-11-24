#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 附件验证器
@Author: Zpp
@Date: 2020-05-28 13:56:03
@LastEditors: Zpp
@LastEditTime: 2020-05-28 15:05:21
'''

params = {
    # 验证字段
    'fields': {
        'document': {
            'name': '文件',
            'type': 'files',
            'required': True,
            'msg': '请选择上传文件'
        },
        'admin_id': {
            'name': '管理员编号',
            'type': 'str',
            'required': True
        },
        'uid[]': {
            'name': '文件编号',
            'type': 'list',
            'required': True
        },
        'status': {
            'name': '类型',
            'type': 'int',
            'required': True
        },
        'folder_id': {
            'name': '所属文件夹',
            'type': 'str'
        },
        'document_id[]': {
            'name': '附件编号',
            'type': 'list',
            'required': True
        },
        'deleted': {
            'name': '是否放入回收站',
            'type': 'boolean',
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
    # 创建附件
    'Create': ['admin_id', 'status', 'uid[]', {
        'field': 'folder_id',
        'default': None
    }, 'document'],
    # 放入回收站
    'Retrieve': ['document_id[]', 'deleted'],
    # 查询附件列表
    'Query': [{
        'field': 'status',
        'required': False
    }, {
        'field': 'deleted',
        'required': False
    }, 'folder_id', 'page', 'page_size', 'order_by'],
    # 删除附件
    'Del': ['document_id[]']
}
