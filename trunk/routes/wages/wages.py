#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录API
@Author: Zpp
@Date: 2020-04-10 14:17:37
@LastEditors: Zpp
@LastEditTime: 2020-04-17 09:56:05
'''
from flask import Blueprint, request
from collection.wages.wages import WagesModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_wages = Blueprint('Wages', __name__, url_prefix='/wages/Wages')


@route_wages.route('/ImportWages', methods=['POST'])
@auth.login_required
@validate_current_access
def ImportWages():
    file = request.files.get('file')
    if not file:
        return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = WagesModel().ImportWagesRequest(file, request.form.get('payment_time'))
    
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_wages.route('/ImportAttendance', methods=['POST'])
# @auth.login_required
# @validate_current_access
def ImportAttendance():
    # file = request.files.get('file')
    # if not file:
    #     return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = WagesModel().ImportAttendanceRequest(None, request.form.get('attendance_time'))
    
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_wages.route('/DelWages', methods=['POST'])
@auth.login_required
@validate_current_access
def DelWages():
    result = WagesModel().DelWagesRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_wages.route('/QueryWagesByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryWagesByParam():
    params = {}
    Ary = ['name', 'company', 'payment_time']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = WagesModel().QueryWagesByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
