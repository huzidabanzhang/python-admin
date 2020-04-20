#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录API
@Author: Zpp
@Date: 2020-04-10 14:17:37
@LastEditors: Zpp
@LastEditTime: 2020-04-20 14:28:54
'''
from flask import Blueprint, request
from collection.v2.salary import SalaryModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_salary = Blueprint('Salary', __name__, url_prefix='/v2/Salary')


@route_salary.route('/ImportSalary', methods=['POST'])
@auth.login_required
@validate_current_access
def ImportSalary():
    file = request.files.get('file')
    if not file:
        return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = SalaryModel().ImportSalaryRequest(file, request.form.get('payment_time'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/DelSalary', methods=['POST'])
@auth.login_required
@validate_current_access
def DelSalary():
    result = SalaryModel().DelSalaryRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/QuerySalaryByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QuerySalaryByParam():
    params = {}
    Ary = ['name', 'company', 'payment_time']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = SalaryModel().QuerySalaryByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/ImportAttendance', methods=['POST'])
@auth.login_required
@validate_current_access
def ImportAttendance():
    file = request.files.get('file')
    if not file:
        return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = SalaryModel().ImportAttendanceRequest(file, request.form.get('attendance_time'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/DelAttendance', methods=['POST'])
@auth.login_required
@validate_current_access
def DelAttendance():
    result = SalaryModel().DelAttendanceRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/QueryAttendanceByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryAttendanceByParam():
    params = {}
    Ary = ['name', 'attendance_time']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = SalaryModel().QueryAttendanceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
