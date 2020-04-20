#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资验证器
@Author: Zpp
@Date: 2020-04-20 14:35:28
@LastEditors: Zpp
@LastEditTime: 2020-04-20 14:54:09
'''


params = {
    # 获取验证短信
    'GetCode': [
        {
            'name': 'phone',
            'type': 'phone',
            'required': True,
            'help_msg': u'手机号格式错误',
            'required_msg': u'请输入手机号'
        }
    ]
}
