#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 权限API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2020-05-29 14:29:30
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
        is_disabled=request.form.get('is_disabled')
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
    if request.form.get('is_disabled'):
        params['is_disabled'] = request.form.get('is_disabled')

    result = RoleModel().QueryRoleByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
