#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 路由API
@Author: Zpp
@Date: 2019-09-11 16:51:59
@LastEditTime: 2019-11-18 15:49:35
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.route import RouteModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_route = Blueprint('Route', __name__, url_prefix='/v1/Route')


@route_route.route('/CreateRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateRoute():
    params = {
        'parentId': request.form.get('parentId', '0'),
        'name': request.form.get('name'),
        'title': request.form.get('title'),
        'path': request.form.get('path'),
        'component': request.form.get('component'),
        'componentPath': request.form.get('componentPath'),
        'cache': True if request.form.get('cache') == 'true' else False
    }

    result = RouteModel().CreateRouteRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_route.route('/LockRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def LockRoute():
    result = RouteModel().LockRouteRequest(
        route_id=request.form.getlist('route_id[]'),
        isLock=True if request.form.get('isLock') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_route.route('/ModifyRoute', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyRoute():
    params = {
        'parentId': request.form.get('parentId', '0'),
        'name': request.form.get('name'),
        'title': request.form.get('title'),
        'path': request.form.get('path'),
        'component': request.form.get('component'),
        'componentPath': request.form.get('componentPath'),
        'cache': True if request.form.get('cache') == 'true' else False
    }

    result = RouteModel().ModifyRouteRequest(route_id=request.form.get('route_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_route.route('/QueryRouteByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryRouteByParam():
    params = {}
    if request.form.get('isLock'):
        params['isLock'] = True if request.form.get('isLock') == 'true' else False
    if request.form.get('name'):
        params['name'] = request.form.get('name')

    result = RouteModel().QueryRouteByParamRequest(params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
