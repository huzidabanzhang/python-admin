#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-11 16:51:59
@LastEditTime: 2019-09-18 10:49:23
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.route import RouteModel
from ..token_auth import auth, validate_current_access
from libs.error_code import ResultDeal

route_route = Blueprint('Route', __name__, url_prefix='/v1/Route')


@route_route.route('/CreateRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateRoute():
    params = {
        'menu_id': request.form.get('menu_id'),
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'description': request.form.get('description'),
        'permission': request.form.get('permission') or 1
    }

    result = RouteModel().CreateRouteRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_route.route('/LockRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def LockRoute():
    result = RouteModel().LockRouteRequest(route_id=request.form.getlist('route_id'))
    return ResultDeal(data=result)


@route_route.route('/ModifyRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRoute():
    params = {}
    Str = ['menu_id', 'name', 'path', 'description', 'permission']
    Int = ['menu_id', 'permission']
    for i in Str:
        if request.form.get(i):
            params[i] = int(request.form.get(i)) if i in Int else request.form.get(i)

    result = RouteModel().ModifyRouteRequest(route_id=request.form.get('route_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_route.route('/QueryRouteByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryRouteByParam():
    result = RouteModel().QueryRouteByParamRequest()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
