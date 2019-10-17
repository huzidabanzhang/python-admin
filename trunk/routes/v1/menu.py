#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 菜单API
@Author: Zpp
@Date: 2019-09-10 16:16:54
@LastEditTime: 2019-10-15 14:45:00
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.menu import MenuModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_menu = Blueprint('Menu', __name__, url_prefix='/v1/Menu')


@route_menu.route('/CreateMenu', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateMenu():
    params = {
        'parentId': request.form.get('parentId', '0'),
        'title': request.form.get('title'),
        'path': request.form.get('path'),
        'icon': request.form.get('icon'),
        'sort': request.form.get('sort'),
        'type': request.form.get('type', 1)
    }

    result = MenuModel().CreateMenuRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/LockMenu', methods=['POST'])
@auth.login_required
@validate_current_access
def LockMenu():
    result = MenuModel().LockMenuRequest(menu_id=request.form.getlist('menu_id'))
    return ResultDeal(data=result)


@route_menu.route('/GetMenu/<menu_id>', methods=['GET'])
@auth.login_required
@validate_current_access
def GetMenu(menu_id):
    result = MenuModel().GetMenuRequest(menu_id=menu_id)
    return ResultDeal(data=result)


@route_menu.route('/ModifyMenu', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyMenu():
    params = request.form
    Int = ['sort', 'type']
    for i in params:
        if i in Int:
            params[i] = int(params[i])

    result = MenuModel().ModifyMenuRequest(menu_id=request.form.get('menu_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/QueryMenuByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryMenuByParam():
    result = MenuModel().QueryMenuByParamRequest()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
