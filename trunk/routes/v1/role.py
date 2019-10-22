#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 权限API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2019-10-22 16:12:36
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.role import RoleModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
import uuid

route_role = Blueprint('Role', __name__, url_prefix='/v1/Role')


@route_role.route('/CreateRole', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateRole():
    params = {
        'role_id': uuid.uuid4(),
        'name': request.form.get('name'),
        'menu_id': request.form.getlist('menu_id[]'),
        'route_id': request.form.getlist('route_id[]')
    }

    result = RoleModel().CreateRoleRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/LockRole', methods=['POST'])
@auth.login_required
@validate_current_access
def LockRole():
    result = RoleModel().LockRoleRequest(role_id=request.form.getlist('role_id[]'))
    return ResultDeal(data=result)


@route_role.route('/ModifyRole', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRole():
    result = RoleModel().ModifyRoleRequest(role_id=request.form.get('role_id'), name=request.form.get('name'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/ModifyRoleToRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRoleToRoute():
    result = RoleModel().ModifyRoleToRoute(role_id=request.form.get('role_id'), route_id=request.form.getlist('route_id[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/ModifyRoleToMenu', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRoleToMenu():
    result = RoleModel().ModifyRoleToMenu(role_id=request.form.get('role_id'), menu_id=request.form.getlist('menu_id[]')) 

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/QueryRoleByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryRoleByParam():
    params = {}
    if request.form.get('isLock'):
        params['isLock'] = True if request.form.get('isLock') == 'true' else False

    result = RoleModel().QueryRoleByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
