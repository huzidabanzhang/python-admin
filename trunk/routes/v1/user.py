#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2019-09-06 14:19:29
@LastEditTime: 2019-09-17 15:38:10
@LastEditors: Zpp
'''
from flask import Blueprint, request, make_response, session
from collection.user import UserModel
from ..token_auth import auth, generate_auth_token
from libs.error_code import ResultDeal
from libs.captcha import Captcha
from io import BytesIO

route_user = Blueprint('User', __name__, url_prefix='/User')


@route_user.route('/CreateDrop', methods=['POST'])
def CreateDrop():
    result = UserModel().CreateDropRequest()
    return ResultDeal(msg=True)


@route_user.route('/Captcha', methods=['GET'])
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


@route_user.route('/Login', methods=['POST'])
def Login():
    # 验证码校验
    captcha = request.form.get('code')
    if not captcha:
        return ResultDeal(msg=u'请输入验证码', code=-1)
    
    if session.get('Captcha').lower() != captcha.lower():
        return ResultDeal(msg=u'验证码不正确', code=-1)

    result = UserModel().GetUserRequest(
        username=request.form.get('username'),
        password=request.form.get('password')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    token = generate_auth_token({
        'username': result['username'],
        'user_id': result['user_id'],
        'role_id': result['role_id'],
        'password': result['password'],
        'nickname': result['nickname']
    })

    return ResultDeal(data={
        'token': token,
        'routes': result['routes'],
        'menus': result['menus']
    })


@route_user.route('/CreateUser', methods=['POST'])
@auth.login_required
def CreateUser():
    params = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'nickname': request.form.get('nickname') or '',
        'sex': request.form.get('sex') or 1,
        'role_id': request.form.get('role_id') or 1
    }

    result = UserModel().CreateUserRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_user.route('/LockUser', methods=['POST'])
@auth.login_required
def LockUser():
    result = UserModel().LockUserRequest(user_id=request.form.getlist('user_id'))
    return ResultDeal(data=result)


@route_user.route('/ModifyUser', methods=['POST'])
@auth.login_required
def ModifyUser():
    params = {}
    Str = ['username', 'nickname', 'sex', 'role_id']
    Int = ['sex', 'role_id']
    for i in Str:
        if request.form.get(i):
            params[i] = int(request.form.get(i)) if i in Int else request.form.get(i)

    result = UserModel().ModifyUserRequest(user_id=request.form.get('user_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_user.route('/QueryUserByParam', methods=['POST'])
@auth.login_required
def QueryUserByParam():
    params = {}
    Str = ['username', 'nickname', 'sex', 'role_id', 'isLock']
    Int = ['sex', 'role_id', 'isLock']
    for i in Str:
        if request.form.get(i):
            params[i] = int(request.form.get(i)) if i in Int else request.form.get(i)

    result = UserModel().QueryUserByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by') if request.form.get('order_by') else None
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
