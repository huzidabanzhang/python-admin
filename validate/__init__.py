#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 验证器
@Author: Zpp
@Date: 2020-04-20 13:43:42
@LastEditors: Zpp
@LastEditTime: 2020-05-29 13:47:57
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

    def validate_min_max(self, value, i):
        '''
        验证字段最大最小值
        '''
        error = None

        if i.has_key('max'):
            if (value if type(value) != list else len(value)) > i:
                error = u'%s最多不能超过%s个' % (i['name'], i['max'])

        if i.has_key('min'):
            if (value if type(value) != list else len(value)) < i:
                error = u'%s不能少于%s个' % (i['name'], i['min'])

        return error

    def validate_between(self, value, i):
        '''
        验证字段是否在固定值之间
        '''
        error = None

        if type(value) != list and i.has_key('between') and type(i['between']) == list and len(i['between']) == 2:
            if not value in i['between']:
                error = u'%s只能在%s和%s之间' % (i['name'], i['between'][0], i['between'][1])

        return error

    def validate_params(self, value, i, fun):
        '''
        验证字段
        '''
        error = None

        if i['type'] == 'int':
            if type(value) != int:
                error = True

        if i['type'] == 'str':
            if type(value) != str:
                error = True

        if i['type'] == 'boolean':
            if value != 'true' and value != 'false':
                error = True
            else:
                self.boolean_change(value, i['field'])

        if i['type'] == 'list':
            if type(value) != list:
                error = True

        if i['type'] == 'ic':
            if not self.id_card.match(value):
                error = True

        if i['type'] == 'phone':
            if not self.phone.match(value):
                error = True

        if i['type'] == 'email':
            if not self.email.match(value):
                error = True

        if i['type'] == 'time':
            if type(value) != datetime.datetime:
                error = True

        if i['type'] != 'boolean':
            error = self.validate_min_max(value, i)
            if not error:
                error = self.validate_between(value, i)

        if error == True:
            return ResultDeal(code=-1, msg=u'%s格式错误' % i['name'])
        elif error == None:
            if i.has_key('default') and not value:
                self.add_default(i['default'], i['field'])
        else:
            return ResultDeal(code=-1, msg=error)

    def add_default(self, default, f):
        '''
        添加默认值
        '''
        r = request.form.copy()
        r[f] = default
        request.form = r

    def boolean_change(self, value, f):
        '''
        前端布尔值改为py的布尔值
        '''
        r = request.form.copy()
        r[f] = True if value == 'true' else False
        request.form = r

    def get_data(self, t, f):
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

    def get_field(self, value, params=None):
        '''
        获取字段详情
        '''
        data = None
        if self.params['fields'].has_key(value):
            data = self.params['fields'][value]
            if params:
                for i in params:
                    data[i] = params[i]

        return data

    def form(self, args):
        '''
        验证表单字段
        '''
        def validate(f):
            def one():
                try:
                    if self.params.has_key(args):
                        for i in self.params[args]:
                            field = None

                            if type(i) == dict:
                                if i.has_key('field'):
                                    field = self.get_field(i['field'], i)
                            else:
                                field = self.get_field(i)
                                field['field'] = i

                            if not field:
                                continue
                            else:
                                value = self.get_data(field['type'], field['field'])

                                if not field.has_key('required') or not field['required']:
                                    if value:
                                        self.validate_params(value, field, f)
                                    else:
                                        if field.has_key('default'):
                                            self.add_default(field['default'], field['field'])
                                else:
                                    if not value:
                                        if field.has_key('default'):
                                            self.add_default(field['default'], field['field'])
                                        else:
                                            if field.has_key('msg'):
                                                return ResultDeal(code=-1, msg=field['msg'])
                                            else:
                                                return ResultDeal(code=-1, msg=u'请填写%s' % field['name'])
                                    else:
                                        self.validate_params(value, field, f)

                    return f()
                except Exception as e:
                    print e
                    return ResultDeal(code=-1, msg=e.message)
            return one

        return validate
