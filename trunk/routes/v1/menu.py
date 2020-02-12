#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 菜单API
@Author: Zpp
@Date: 2019-09-10 16:16:54
@LastEditTime : 2020-02-12 14:05:36
@LastEditors  : Please set LastEditors
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
        'parent_id': request.form.get('parent_id', '0'),
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
    result = MenuModel().LockMenuRequest(
        menu_id=request.form.get('menu_id'),
        isLock=True if request.form.get('isLock') == 'true' else False
    )
    
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
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
    params = {
        'parent_id': request.form.get('parent_id', '0'),
        'title': request.form.get('title'),
        'path': request.form.get('path'),
        'icon': request.form.get('icon'),
        'sort': request.form.get('sort'),
        'type': request.form.get('type', 1)
    }

    result = MenuModel().ModifyMenuRequest(menu_id=request.form.get('menu_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_menu.route('/QueryMenuByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryMenuByParam():
    params = {}
    if request.form.get('is_disabled'):
        params['is_disabled'] = True if request.form.get('is_disabled') == 'true' else False
            
    result = MenuModel().QueryMenuByParamRequest(
        params=params, 
        is_interface=True if request.form.get('is_interface') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
