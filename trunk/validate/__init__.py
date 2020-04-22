#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 验证器
@Author: Zpp
@Date: 2020-04-20 13:43:42
@LastEditors: Zpp
@LastEditTime: 2020-04-22 15:00:15
'''
from flask import request
from libs.code import ResultDeal
import re
import datetime

class validate_form():
    '''
    表单验证器
    '''
    def __init__(self, params):
        self.params = params
        self.phone = re.compile('^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$')
        self.id_card = re.compile('^\d{6}(18|19|20)\d{2}(0\d|10|11|12)([0-2]\d|30|31)\d{3}[\dXx]$')
        self.email = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")

    def validate_min_max(self, f, i):
        '''
        验证字段最大最小值
        '''
        error = None

        if i.has_key('max'):
            if f > i:
                error = u'%s超出字符限制' % i['name']

        if i.has_key('min'):
            if f < i:
                error = u'%s不能少于%s个字符' % (i['name'], i['min'])

        return error

    def validate_between(self, f, i):
        '''
        验证字段是否在固定值之间
        '''
        error = None

        if i.has_key('between') and type(i['between']) == list:
            if not f in i['between']:
                error = u'%s不在规定范围内' % i['name']

        return error

    def validate_params(self, f, i, fun):
        '''
        验证字段
        '''
        error = None

        if i['type'] == 'int':
            if type(f) != int:
                error = True

            error = self.validate_min_max(f, i)
            if not error:
                error = self.validate_between(f, i)

        if i['type'] == 'str':
            if type(f) != str:
                error = True

            error = self.validate_min_max(f, i)
            if not error:
                error = self.validate_between(f, i)

        if i['type'] == 'boolean':
            if f != 'true' and f != 'false':
                error = True

        if i['type'] == 'list':
            if type(f) != list:
                error = True

        if i['type'] == 'ic':
            if not self.id_card.match(f):
                error = True
        
        if i['type'] == 'phone':
            if not self.phone.match(f):
                error = True

        if i['type'] == 'email':
            if not self.email.match(f):
                error = True

        if i['type'] == 'time':
            if type(f) != datetime.datetime:
                error = True
                
        if error == True:
            return ResultDeal(code=-1, msg=u'%s格式错误' % i['name'])
        elif error == None:
            if i.has_key('default'):
                self.add_default(f, i['default'])
        else:
            return ResultDeal(code=-1, msg=error)

    def add_default(self, f, default):
        '''
        添加默认值
        '''
        r = request.form.copy()
        r[f] = default
        request.form = r

    def get_data(self, f, t):
        '''
        获取值
        '''
        if t == 'list':
            return request.form.getlist(f)

        if t == 'file':
            return request.files.get(f)

        if t == 'files':
            return request.files.getlist(f)

        return request.form.get(f)

    def form(self, args):
        '''
        验证表单字段
        '''
        def validate(f):
            def one():
                try:
                    if self.params.has_key(args):
                        for i in self.params[args]:
                            data = self.get_data(i['value'], i['type'])
                            
                            if not i.has_key('required') or not i['required']:
                                if data:
                                    self.validate_params(data, i, f)
                                else:
                                    if i.has_key('default'):
                                        self.add_default(i['value'], i['default'])
                            else:
                                if not data:
                                    if i.has_key('msg'):
                                        return ResultDeal(code=-1, msg=i['msg'])
                                    else:
                                        return ResultDeal(code=-1, msg=u'请输入%s' % i['name'])
                                else:
                                    self.validate_params(data, i, f)

                    return f()
                except Exception as e:
                    return ResultDeal(code=-1, msg=e.message)
            return one
        
        return validate
