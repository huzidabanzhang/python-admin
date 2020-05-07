#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资验证器
@Author: Zpp
@Date: 2020-04-20 14:35:28
@LastEditors: Zpp
@LastEditTime: 2020-05-07 14:06:00
'''


params = {
    # 获取验证短信
    'GetCode': [
        {
            'name': u'手机号',
            'value': 'phone',
            'type': 'phone',
            'required': True
        }
    ],
    # 获取openid
    'AddSalary': [
        {
            'name': u'验证码',
            'value': 'code',
            'type': 'int',
            'required': True
        },
        {
            'name': u'身份证',
            'value': 'id_card',
            'type': 'ic',
            'required': True
        },
        {
            'name': u'手机号',
            'value': 'phone',
            'type': 'phone',
            'required': True
        }
    ],
    # 查询工资记录
    'GetSalary': [
        {
            'name': u'openid',
            'value': 'openid',
            'type': 'str',
            'required': True,
            'msg': u'请先注册'
        },
        {
            'name': u'页码',
            'value': 'page',
            'type': 'int',
            'default': 1
        },
        {
            'name': u'条数',
            'value': 'page_size',
            'type': 'int',
            'default': 20
        }
    ],
    # 查询考勤记录
    'GetAttence': [
        {
            'name': u'姓名',
            'value': 'name',
            'type': 'str',
            'required': True
        },
        {
            'name': u'工号',
            'value': 'user_id',
            'type': 'str',
            'required': True
        },
        {
            'name': u'页码',
            'value': 'page',
            'type': 'int',
            'default': 1
        },
        {
            'name': u'条数',
            'value': 'page_size',
            'type': 'int',
            'default': 20
        }
    ],
    # 上传工资记录
    'ImportSalary': [
        {
            'name': u'文件',
            'value': 'file',
            'type': 'file',
            'required': True,
            'msg': u'请选择上传文件'
        },
        {
            'name': u'工资时间',
            'value': 'payment_time',
            'type': 'time',
            'required': True
        }
    ],
    # 上传考勤记录
    'ImportAttendance': [
        {
            'name': u'文件',
            'value': 'file',
            'type': 'file',
            'required': True,
            'msg': u'请选择上传文件'
        },
        {
            'name': u'考勤时间',
            'value': 'attendance_time',
            'type': 'time',
            'required': True
        }
    ],
    # 删除工资记录
    'DelSalary': [
        {
            'name': u'编号',
            'value': 'rid[]',
            'type': 'list',
            'required': True
        }
    ],
    # 删除考勤记录
    'DelAttendance': [
        {
            'name': u'编号',
            'value': 'rid[]',
            'type': 'list',
            'required': True
        }
    ],
    # 获取工资记录列表
    'QuerySalaryByParam': [
        {
            'name': u'姓名',
            'value': 'name',
            'type': 'str'
        },
        {
            'name': u'公司',
            'value': 'company',
            'type': 'str'
        },
        {
            'name': u'工资时间',
            'value': 'payment_time',
            'type': 'time'
        },
        {
            'name': u'页码',
            'value': 'page',
            'type': 'int',
            'default': 1
        },
        {
            'name': u'条数',
            'value': 'page_size',
            'type': 'int',
            'default': 20
        }
    ],
    # 获取考勤记录列表
    'QueryAttendanceByParam': [
        {
            'name': u'姓名',
            'value': 'name',
            'type': 'str'
        },
        {
            'name': u'考勤时间',
            'value': 'attendance_time',
            'type': 'time'
        },
        {
            'name': u'页码',
            'value': 'page',
            'type': 'int',
            'default': 1
        },
        {
            'name': u'条数',
            'value': 'page_size',
            'type': 'int',
            'default': 20
        }
    ],
    # 获取用户列表
    'QueryUserByParam': [
        {
            'name': u'手机号',
            'value': 'phone',
            'type': 'str'
        },
        {
            'name': u'身份证',
            'value': 'id_card',
            'type': 'str'
        },
        {
            'name': u'页码',
            'value': 'page',
            'type': 'int',
            'default': 1
        },
        {
            'name': u'条数',
            'value': 'page_size',
            'type': 'int',
            'default': 20
        }
    ],
    # 删除用户
    'DelUser': [
        {
            'name': u'编号',
            'value': 'rid[]',
            'type': 'list',
            'required': True
        }
    ],
    # 修改用户
    'SetUser': [
        {
            'name': u'编号',
            'value': 'salary_user_id',
            'type': 'str',
            'required': True
        },
        {
            'name': u'手机号',
            'value': 'phone',
            'type': 'phone',
            'required': True
        },
        {
            'name': u'身份证',
            'value': 'id_card',
            'type': 'ic',
            'required': True
        }
    ]
}
