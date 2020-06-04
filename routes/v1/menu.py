#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 菜单API
@Author: Zpp
@Date: 2019-09-10 16:16:54
@LastEditTime: 2020-05-29 14:20:36
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.v1.menu import MenuModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from validate import validate_form
from validate.v1.menu import params

route_menu = Blueprint('Menu', __name__, url_prefix='/v1/Menu')
validate = validate_form(params)


@route_menu.route('/CreateMenu', methods=['POST'], endpoint='CreateMenu')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateMenu():
    result = MenuModel().CreateMenuRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/DelMenu', methods=['POST'], endpoint='DelMenu')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelMenu():
    result = MenuModel().DelMenuRequest(request.form.get('menu_id'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/GetMenuToInterface', methods=['GET'], endpoint='GetMenuToInterface')
@auth.login_required
@validate_current_access
@validate.form('Get')
def GetMenuToInterface():
    result = MenuModel().GetMenuToInterfaceRequest(request.args.get('menu_id'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/ModifyMenu', methods=['POST'], endpoint='ModifyMenu')
@auth.login_required
@validate_current_access
@validate.form('Modify')
def ModifyMenu():
    result = MenuModel().ModifyMenuRequest(request.form.get('menu_id'), request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/QueryMenuByParam', methods=['POST'], endpoint='QueryMenuByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryMenuByParam():
    params = {}
    if request.form.get('disable'):
        params['disable'] = request.form.get('disable')
    if request.form.get('role_id'):
        params['role_id'] = request.form.get('role_id')

    result = MenuModel().QueryMenuByParamRequest(
        params=params,
        is_interface=request.form.get('is_interface')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
