#!/usr/bin/env python
# -*- coding:UTF-8 -*-\
'''
@Description: 权限API
@Author: Zpp
@Date: 2019-09-12 10:30:39
@LastEditTime: 2019-11-18 16:20:06
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.role import RoleModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
import uuid
import json

route_role = Blueprint('Role', __name__, url_prefix='/v1/Role')


@route_role.route('/CreateRole', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateRole():
    params = {
        'role_id': uuid.uuid4(),
        'name': request.form.get('name'),
        'checkKey': request.form.get('checkKey'),
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
    result = RoleModel().LockRoleRequest(
        role_id=request.form.getlist('role_id[]'),
        isLock=True if request.form.get('isLock') == 'true' else False
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
        'checkKey': request.form.get('checkKey'),
        'menu_id': request.form.getlist('menu_id[]'),
        'route_id': request.form.getlist('route_id[]')
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
    if request.form.get('isLock'):
        params['isLock'] = True if request.form.get('isLock') == 'true' else False

    result = RoleModel().QueryRoleByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
