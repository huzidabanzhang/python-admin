#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 管理员API
@Author: Zpp
@Date: 2019-09-06 14:19:29
@LastEditTime: 2020-05-11 14:26:45
@LastEditors: Zpp
'''
from flask import Blueprint, request, make_response, session
from collection.v1.admin import AdminModel
from ..token_auth import auth, generate_auth_token, validate_current_access, get_auth_token
from conf.setting import default
from libs.code import ResultDeal
from libs.captcha import Captcha
from io import BytesIO
from libs.scope import checkDb
import json

route_admin = Blueprint('Admin', __name__, url_prefix='/v1/Admin')


@route_admin.route('/checkDb', methods=['GET'])
def CheckDb():
    result = checkDb()
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/Captcha', methods=['GET'])
def GetCaptcha():
    text, image = Captcha().gen_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    # 存入session
    session['Captcha'] = text
    return resp


@route_admin.route('/Login', methods=['POST'])
def Login():
    # 验证码校验
    captcha = request.form.get('code')
    sesson_captcha = session.get('Captcha')
    if not captcha:
        return ResultDeal(msg=str('请输入验证码'), code=-1)

    if not sesson_captcha:
        return ResultDeal(msg=str('请刷新验证码'), code=-1)

    if session.get('Captcha').lower() != captcha.lower():
        return ResultDeal(msg=str('验证码不正确'), code=-1)

    result = AdminModel().GetAdminRequest(
        username=request.form.get('username'),
        password=request.form.get('password')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    try:
        user = result['user']

        token = generate_auth_token({
            'admin_id': user['admin_id'],
            'password': user['password'],
            'is_admin': True if user['mark'] == default['role_mark'] else False
        })

        session['admin'] = token
        session['username'] = user['username']

        return ResultDeal(data={
            'token': token,
            'menus': result['menus'],
            'interface': result['interface'],
            'info': user
        })
    except Exception as e:
        print e
        return ResultDeal(msg=e.message, code=-1)


@route_admin.route('/Logout', methods=['GET'])
def Logout():
    session.pop('admin')
    return ResultDeal()


@route_admin.route('/CreateAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateAdmin():
    params = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'nickname': request.form.get('nickname', ''),
        'email': request.form.get('email', ''),
        'sex': request.form.get('sex', 1),
        'role_id': request.form.get('role_id'),
        'avatarUrl': request.form.get('avatarUrl', ''),
        'is_disabled': True if request.form.get('is_disabled') == 'true' else False
    }

    result = AdminModel().CreateAdminRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/LockAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def LockAdmin():
    result = AdminModel().LockAdminRequest(
        admin_id=request.form.getlist('admin_id[]'),
        is_disabled=True if request.form.get('is_disabled') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/DelAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def DelAdmin():
    result = AdminModel().DelAdminRequest(
        admins=json.loads(request.form.get('admins'))
    )
    
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_admin.route('/ModifyAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyAdmin():
    params = {
        'password': request.form.get('password'),
        'nickname': request.form.get('nickname'),
        'email': request.form.get('email', ''),
        'sex': int(request.form.get('sex')),
        'avatarUrl': request.form.get('avatarUrl', ''),
        'role_id': request.form.get('role_id'),
        'is_disabled': True if request.form.get('is_disabled') == 'true' else False
    }

    result = AdminModel().ModifyAdminRequest(admin_id=request.form.get('admin_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    token = session.get('admin')
    info = get_auth_token(token)
    if info['admin_id'] == request.form.get('admin_id'):
        token = generate_auth_token({
            'admin_id': result['admin_id'],
            'password': result['password'],
            'is_admin': True if result['mark'] == default['role_mark'] else False
        })

        session['admin'] = token
        session['username'] = result['username']

        return ResultDeal(data={
            'user': result,
            'token': token,
            'is_self': True
        })
    
    return ResultDeal(data={
        'user': result,
        'token': None,
        'is_self': False
    })


@route_admin.route('/QueryAdminByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryAdminByParam():
    params = {}
    if request.form.get('is_disabled'):
        params['is_disabled'] = True if request.form.get('is_disabled') == 'true' else False
    if request.form.get('role_id'):
        params['role_id'] = request.form.get('role_id')

    result = AdminModel().QueryAdminByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
