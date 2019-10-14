#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口API
@Author: Zpp
@Date: 2019-10-14 13:50:25
@LastEditors: Zpp
@LastEditTime: 2019-10-14 14:36:48
'''
from flask import Blueprint, request
from collection.interface import InterfaceModel
from ..token_auth import auth, validate_current_access
from libs.error_code import ResultDeal

route_interface = Blueprint('Interface', __name__, url_prefix='/v1/Interface')


@route_interface.interface('/CreateInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateInterface():
    params = {
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'method': request.form.get('method'),
        'description': request.form.get('description'),
        'menu_id': int(request.form.get('menu_id'))
    }

    result = InterfaceModel().CreateInterfaceRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.interface('/LockInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def LockInterface():
    result = InterfaceModel().LockInterfaceRequest(interface_id=request.form.getlist('interface_id'))
    return ResultDeal(data=result)


@route_interface.interface('/ModifyInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyInterface():
    params = request.form
    Int = ['menu_id']
    for i in params:
        if i in Int:
            params[i] = int(params[i])

    result = InterfaceModel().ModifyInterfaceRequest(interface_id=request.form.get('interface_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.interface('/QueryInterfaceByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryInterfaceByParam():
    params = request.form
    Int = ['menu_id']
    Bool = ['isLock']
    for i in params:
        if i in Int:
            params[i] = int(params[i])
        if i in Bool:
            params[i] = True if params[i] == 'true' else False

    result = InterfaceModel().QueryInterfaceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
