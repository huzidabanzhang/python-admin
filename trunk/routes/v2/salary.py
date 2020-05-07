#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录API
@Author: Zpp
@Date: 2020-04-10 14:17:37
@LastEditors: Zpp
@LastEditTime: 2020-05-07 14:03:28
'''
from flask import Blueprint, request
from collection.v2.salary import SalaryModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from validate import validate_form
from validate.v2.salary import params

route_salary = Blueprint('Salary', __name__, url_prefix='/v2/Salary')
validate = validate_form(params)


@route_salary.route('/ImportSalary', methods=['POST'], endpoint='ImportSalary')
@auth.login_required
@validate_current_access
@validate.form('ImportSalary')
def ImportSalary():
    result = SalaryModel().ImportSalaryRequest(request.files.get('file'), request.form.get('payment_time'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/DelSalary', methods=['POST'], endpoint='DelSalary')
@auth.login_required
@validate_current_access
@validate.form('DelSalary')
def DelSalary():
    result = SalaryModel().DelSalaryRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/QuerySalaryByParam', methods=['POST'], endpoint='QuerySalaryByParam')
@auth.login_required
@validate_current_access
@validate.form('QuerySalaryByParam')
def QuerySalaryByParam():
    params = {}
    Ary = ['name', 'company', 'payment_time']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = SalaryModel().QuerySalaryByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/ImportAttendance', methods=['POST'], endpoint='ImportAttendance')
@auth.login_required
@validate_current_access
@validate.form('ImportAttendance')
def ImportAttendance():
    result = SalaryModel().ImportAttendanceRequest(request.files.get('file'), request.form.get('attendance_time'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/DelAttendance', methods=['POST'], endpoint='DelAttendance')
@auth.login_required
@validate_current_access
@validate.form('DelAttendance')
def DelAttendance():
    result = SalaryModel().DelAttendanceRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/QueryAttendanceByParam', methods=['POST'], endpoint='QueryAttendanceByParam')
@auth.login_required
@validate_current_access
@validate.form('QueryAttendanceByParam')
def QueryAttendanceByParam():
    params = {}
    Ary = ['name', 'attendance_time']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = SalaryModel().QueryAttendanceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/SetUser', methods=['POST'], endpoint='SetUser')
@auth.login_required
@validate_current_access
@validate.form('SetUser')
def SetUser():
    result = SalaryModel().SetUserRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/DelUser', methods=['POST'], endpoint='DelUser')
@auth.login_required
@validate_current_access
@validate.form('DelUser')
def DelUser():
    result = SalaryModel().DelUserRequest(request.form.getlist('rid[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_salary.route('/QueryUserByParam', methods=['POST'], endpoint='QueryUserByParam')
@auth.login_required
@validate_current_access
@validate.form('QueryUserByParam')
def QueryUserByParam():
    params = {}
    Ary = ['phone', 'id_card']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = SalaryModel().QueryUserByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
