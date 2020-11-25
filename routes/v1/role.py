#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 鉴权API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2020-06-05 09:52:23
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.v1.role import RoleModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from validate import validate_form
from validate.v1.role import params
import json

route_role = Blueprint('Role', __name__, url_prefix='/v1/Role')
validate = validate_form(params)


@route_role.route('/CreateRole', methods=['POST'], endpoint='CreateRole')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateRole():
    result = RoleModel().CreateRoleRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/LockRole', methods=['POST'], endpoint='LockRole')
@auth.login_required
@validate_current_access
@validate.form('Lock')
def LockRole():
    result = RoleModel().LockRoleRequest(
        role_id=request.form.getlist('role_id[]'),
        disable=request.form.get('disable')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/DelRole', methods=['POST'], endpoint='DelRole')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelRole():
    result = RoleModel().DelRoleRequest(
        role_id=request.form.getlist('role_id[]')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/ModifyRole', methods=['POST'], endpoint='ModifyRole')
@auth.login_required
@validate_current_access
@validate.form('Modify')
def ModifyRole():
    result = RoleModel().ModifyRoleRequest(request.form.get('role_id'), request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/QueryRoleByParam', methods=['POST'], endpoint='QueryRoleByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryRoleByParam():
    params = {}
    if request.form.get('disable') != None:
        params['disable'] = request.form.get('disable')

    result = RoleModel().QueryRoleByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
