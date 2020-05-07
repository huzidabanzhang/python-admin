#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资查询API
@Author: Zpp
@Date: 2020-04-13 13:07:43
@LastEditors: Zpp
@LastEditTime: 2020-05-07 14:53:21
'''
from flask import Blueprint, request, session
from collection.v2.salary import SalaryModel
from libs.code import ResultDeal
from conf.aliyun import wx_info
from validate import validate_form
from validate.v2.salary import params
import urllib
import json
import datetime

route_salary_user = Blueprint('SalaryUser', __name__, url_prefix='/v2/SalaryUser')
validate = validate_form(params)


@route_salary_user.route('/GetCode', methods=['POST'], endpoint='GetCode')
@validate.form('GetCode')
def GetCode():
    Code = session.get('Code')

    if Code and (datetime.datetime.now() - Code['time']).seconds < 60:
        return ResultDeal(msg=u'请在%s秒后重新获取验证码' % (60 - (datetime.datetime.now() - Code['time']).seconds), code=-1)

    result = SalaryModel().GetCodeRequest(request.form.get('phone'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary_user.route('/AddSalary', methods=['POST'], endpoint='AddSalary')
@validate.form('AddSalary')
def AddSalary():
    Code = session.get('Code')

    if not Code:
        return ResultDeal(msg=u'请获取验证码', code=-1)

    if (datetime.datetime.now() - Code['time']).seconds > 5 * 60:
        return ResultDeal(msg=u'验证码已过期, 请重新获取', code=-1)

    if Code['code'] != request.form.get('code'):
        return ResultDeal(msg=u'验证码不正确', code=-1)

    result = SalaryModel().AddSalaryRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result['openid'])


@route_salary_user.route('/GetSalary', methods=['POST'], endpoint='GetSalary')
@validate.form('GetSalary')
def GetSalary():
    result = SalaryModel().GetSalaryRequest(
        openid=request.form.get('openid'),
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary_user.route('/GetAttence', methods=['POST'], endpoint='GetAttence')
@validate.form('GetAttence')
def GetAttence():
    result = SalaryModel().GetAttendanceRequest(
        params=request.form,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
