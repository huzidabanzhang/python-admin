#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 管理员API
@Author: Zpp
@Date: 2019-09-06 14:19:29
@LastEditTime: 2019-10-17 16:19:12
@LastEditors: Zpp
'''
from flask import Blueprint, request, make_response, session
from collection.admin import AdminModel
from ..token_auth import auth, generate_auth_token, validate_current_access
from libs.code import ResultDeal
from libs.captcha import Captcha
from io import BytesIO

route_admin = Blueprint('Admin', __name__, url_prefix='/v1/Admin')


@route_admin.route('/CreateDrop', methods=['GET'])
def CreateDrop():
    result = AdminModel().CreateDropRequest()
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data={
        'username': 'Admin',
        'password': '123456'
    })


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
        return ResultDeal(msg=u'请输入验证码', code=-1)

    if not sesson_captcha:
        return ResultDeal(msg=u'请刷新验证码', code=-1)
    
    if session.get('Captcha').lower() != captcha.lower():
        return ResultDeal(msg=u'验证码不正确', code=-1)

    result = AdminModel().GetAdminRequest(
        username=request.form.get('username'),
        password=request.form.get('password')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    try:
        token = generate_auth_token({
            'admin_id': result['admin_id'],
            'password': result['password'],
            'is_admin': True if result['role_id'] == 1 else False
        })

        session['admin'] = token
        session['username'] = result['username']
        return ResultDeal(data={
            'token': token,
            'routes': result['routes'],
            'menus': result['menus'],
            'interface': result['interface'],
            'info': {
                'name': result['nickname'] if result['nickname'] else result['username'],
                'user_id': result['admin_id'],
                'avatarUrl': result['avatarUrl'],
                'key': result['password']
            }
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
        'sex': request.form.get('sex', 1),
        'role_id': request.form.get('role_id', 1),
        'avatarUrl': request.form.get('avatarUrl', '')
    }

    result = AdminModel().CreateAdminRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/LockAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def LockAdmin():
    result = AdminModel().LockAdminRequest(admin_id=request.form.getlist('admin_id'))
    return ResultDeal(data=result)


@route_admin.route('/ModifyAdmin', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyAdmin():
    params = request.form
    Int = ['sex', 'role_id']
    for i in params:
        if i in Int:
            params[i] = int(params[i])

    result = AdminModel().ModifyAdminRequest(admin_id=request.form.get('admin_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/QueryAdminByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryAdminByParam():
    params = request.form
    Int = ['sex', 'role_id']
    Bool = ['isLock']
    for i in params:
        if i in Int:
            params[i] = int(params[i])
        if i in Bool:
            params[i] = True if params[i] == 'true' else False

    result = AdminModel().QueryAdminByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
