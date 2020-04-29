#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 权限API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2020-04-29 15:23:04
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.v1.role import RoleModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
import json

route_role = Blueprint('Role', __name__, url_prefix='/v1/Role')


@route_role.route('/CreateRole', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateRole():
    params = {
        'name': request.form.get('name'),
        'mark': request.form.get('mark'),
        'is_disabled': True if request.form.get('is_disabled') == 'true' else False,
        'menu_id': request.form.getlist('menu_id[]'),
        'interface_id': request.form.getlist('interface_id[]')
    }

    result = RoleModel().CreateRoleRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/LockRole', methods=['POST'])
@auth.login_required
@validate_current_access
def LockRole():
    result = RoleModel().LockRoleRequest(
        role_id=request.form.getlist('role_id[]'),
        is_disabled=True if request.form.get('is_disabled') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_role.route('/DelRole', methods=['POST'])
@auth.login_required
@validate_current_access
def DelRole():
    result = RoleModel().DelRoleRequest(
        role_id=request.form.getlist('role_id[]')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_role.route('/ModifyRole', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRole():
    params = {
        'name': request.form.get('name'),
        'mark': request.form.get('mark'),
        'is_disabled': True if request.form.get('is_disabled') == 'true' else False,
        'menu_id': request.form.getlist('menu_id[]'),
        'interface_id': request.form.getlist('interface_id[]')
    }
    result = RoleModel().ModifyRoleRequest(role_id=request.form.get('role_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/QueryRoleByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryRoleByParam():
    params = {}
    if request.form.get('is_disabled'):
        params['is_disabled'] = True if request.form.get('is_disabled') == 'true' else False

    result = RoleModel().QueryRoleByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
