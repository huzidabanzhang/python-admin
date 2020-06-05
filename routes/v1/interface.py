#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口API
@Author: Zpp
@Date: 2019-10-14 13:50:25
@LastEditors: Zpp
@LastEditTime: 2020-06-05 09:48:53
'''
from flask import Blueprint, request
from collection.v1.interface import InterfaceModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from validate import validate_form
from validate.v1.interface import params
import json

route_interface = Blueprint('Interface', __name__, url_prefix='/v1/Interface')
validate = validate_form(params)


@route_interface.route('/CreateInterface', methods=['POST'], endpoint='CreateInterface')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateInterface():
    result = InterfaceModel().CreateInterfaceRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/LockInterface', methods=['POST'], endpoint='LockInterface')
@auth.login_required
@validate_current_access
@validate.form('Lock')
def LockInterface():
    result = InterfaceModel().LockInterfaceRequest(
        request.form.getlist('interface_id[]'),
        request.form.get('disable')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/DelInterface', methods=['POST'], endpoint='DelInterface')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelInterface():
    result = InterfaceModel().DelInterfaceRequest(request.form.getlist('interface_id[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/ModifyInterface', methods=['POST'], endpoint='ModifyInterface')
@auth.login_required
@validate_current_access
@validate.form('Modify')
def ModifyInterface():
    result = InterfaceModel().ModifyInterfaceRequest(request.form.get('interface_id'), request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/QueryInterfaceByParam', methods=['POST'], endpoint='QueryInterfaceByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryInterfaceByParam():
    params = {}
    Ary = ['name', 'method', 'disable']
    for i in Ary:
        if request.form.get(i) != None:
            params[i] = request.form.get(i)

    result = InterfaceModel().QueryInterfaceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
