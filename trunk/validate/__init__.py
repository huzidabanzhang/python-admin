#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 验证器
@Author: Zpp
@Date: 2020-04-20 13:43:42
@LastEditors: Zpp
@LastEditTime: 2020-04-20 16:51:11
'''
from flask import request
from libs.code import ResultDeal

class validate_form():
    '''
    表单验证器
    '''
    def __init__(self, params):
        self.params = params

    def validate_params(self, f, i):
        '''
        验证字段
        '''
        if i['type'] == 'int':
            if type(f) != int:
                return ResultDeal(code=-1, msg=i['help_msg'])

        if i['type'] == 'str':
            if type(f) != str:
                return ResultDeal(code=-1, msg=i['help_msg'])

        if i['type'] == 'boolean':
            if f != 'true' and f != 'false':
                return ResultDeal(code=-1, msg=i['help_msg'])

        

    def form(self, args):
        '''
        验证表单字段
        '''
        def validate(f):
            def one():
                if self.params.has_key(args):
                    for i in self.params[args]:
                        if not i.has_key('required') or not i['required']:
                            if request.form.get(i['name']):
                                return self.validate_params(request.form.get(i['name']), i)
                        else:
                            if not request.form.get(i['name']):
                                return ResultDeal(code=-1, msg=i['required_msg'])
                            else:
                                return self.validate_params(request.form.get(i['name']), i)

                return f
            return one
        
        return validate
