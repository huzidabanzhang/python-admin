#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 权限API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2019-09-18 09:12:57
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.role import RoleModel
from ..token_auth import auth, generate_auth_token
from libs.error_code import ResultDeal

route_role = Blueprint('Role', __name__, url_prefix='/v1/Role')


@route_role.route('/CreateRole', methods=['POST'])
@auth.login_required
def CreateRole():
    params = {
        'name': request.form.get('name'),
        'type': request.form.get('type')
    }

    result = RoleModel().CreateRoleRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/LockRole', methods=['POST'])
@auth.login_required
def LockRole():
    result = RoleModel().LockRoleRequest(role_id=request.form.getlist('role_id'))
    return ResultDeal(data=result)


@route_role.route('/ModifyRole', methods=['POST'])
@auth.login_required
def ModifyRole():
    result = RoleModel().ModifyRoleRequest(role_id=request.form.get('role_id'), name=request.form.get('name'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/ModifyRoleToRoute', methods=['POST'])
@auth.login_required
def ModifyRoleToRoute():
    result = RoleModel().ModifyRoleToRoute(role_id=request.form.get('role_id'), route_id=request.form.getlist('route_id'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/ModifyRoleToMenu', methods=['POST'])
@auth.login_required
def ModifyRoleToMenu():
    result = RoleModel().ModifyRoleToMenu(role_id=request.form.get('role_id'), menu_id=request.form.getlist('menu_id')) 

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_role.route('/QueryRoleByParam', methods=['POST'])
@auth.login_required
def QueryRoleByParam():
    result = RoleModel().QueryRoleByParamRequest()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
