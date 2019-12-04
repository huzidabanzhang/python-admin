#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口API
@Author: Zpp
@Date: 2019-10-14 13:50:25
@LastEditors: Zpp
@LastEditTime: 2019-10-14 16:46:14
'''
from flask import Blueprint, request
from collection.interface import InterfaceModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_interface = Blueprint('Interface', __name__, url_prefix='/v1/Interface')


@route_interface.route('/CreateInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateInterface():
    params = {
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'method': request.form.get('method'),
        'description': request.form.get('description'),
        'menu_id': request.form.get('menu_id'),
        'identification': request.form.get('identification')
    }

    result = InterfaceModel().CreateInterfaceRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/LockInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def LockInterface():
    result = InterfaceModel().LockInterfaceRequest(interface_id=request.form.getlist('interface_id[]'), isLock=request.form.get('isLock'))
    return ResultDeal(data=result)


@route_interface.route('/ModifyInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyInterface():
    params = {
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'method': request.form.get('method'),
        'description': request.form.get('description'),
        'menu_id': request.form.get('menu_id'),
        'identification': request.form.get('identification')
    }

    result = InterfaceModel().ModifyInterfaceRequest(interface_id=request.form.get('interface_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/QueryInterfaceByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryInterfaceByParam():
    params = {}
    if request.form.get('isLock'):
        params['isLock'] = True if request.form.get('isLock') == 'true' else False
    Ary = ['name', 'method']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = InterfaceModel().QueryInterfaceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
