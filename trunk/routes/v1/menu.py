#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:16:54
@LastEditTime: 2019-09-12 10:29:06
@LastEditors: Zpp
'''
from flask import Blueprint, request
from collection.menu import MenuModel
from ..token_auth import auth, generate_auth_token
from libs.error_code import ResultDeal

route_menu = Blueprint('Menu', __name__, url_prefix='/Menu')


@route_menu.route('/CreateMenu', methods=['POST'])
@auth.login_required
def CreateMenu():
    params = {
        'parentId': request.form.get('parentId') or 0,
        'title': request.form.get('title'),
        'path': request.form.get('path'),
        'icon': request.form.get('icon'),
        'sort': request.form.get('sort'),
        'permission': request.form.get('permission') or 1
    }

    result = MenuModel().CreateMenuRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/LockMenu', methods=['POST'])
@auth.login_required
def LockMenu():
    result = MenuModel().LockMenuRequest(menu_id=request.form.getlist('menu_id'))
    return ResultDeal(data=result)


@route_menu.route('/GetMenu', methods=['POST'])
@auth.login_required
def GetMenu():
    result = MenuModel().GetMenuRequest(menu_id=request.form.get('menu_id'))
    return ResultDeal(data=result)


@route_menu.route('/ModifyMenu', methods=['POST'])
@auth.login_required
def ModifyMenu():
    params = {}
    Str = ['parentId', 'title', 'path', 'icon', 'sort', 'permission']
    Int = ['sort', 'parentId', 'permission']
    for i in Str:
        if request.form.get(i):
            params[i] = int(request.form.get(i)) if i in Int else request.form.get(i)

    result = MenuModel().ModifyMenuRequest(menu_id=request.form.get('menu_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/QueryMenuByParam', methods=['POST'])
@auth.login_required
def QueryMenuByParam():
    result = MenuModel().QueryMenuByParamRequest()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
