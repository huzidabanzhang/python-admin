#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 用户API
@Author: Zpp
@Date: 2019-09-06 14:19:29
@LastEditTime: 2019-10-15 11:00:57
@LastEditors: Zpp
'''
from flask import Blueprint, request, make_response, session
from collection.user import UserModel
from ..token_auth import auth, generate_auth_token, validate_current_access
from libs.error_code import ResultDeal, RecordLog
from libs.captcha import Captcha
from io import BytesIO

route_user = Blueprint('User', __name__, url_prefix='/v1/User')


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
    sesson_captcha = session.get('Captcha')
    if not captcha:
        return ResultDeal(msg=u'请输入验证码', code=-1)

    if not sesson_captcha:
        return ResultDeal(msg=u'请刷新验证码', code=-1)
    
    if session.get('Captcha').lower() != captcha.lower():
        return ResultDeal(msg=u'验证码不正确', code=-1)

    result = UserModel().GetUserRequest(
        username=request.form.get('username'),
        password=request.form.get('password')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    try:
        token = generate_auth_token({
            'user_id': result['user_id'],
            'password': result['password'],
            'is_admin': True if result['role_id'] == 1 else False
        })

        session['User'] = token
        return ResultDeal(data={
            'token': token,
            'routes': result['routes'],
            'menus': result['menus'],
            'interface': result['interface'],
            'info': {
                'name': result['nickname'] if result['nickname'] else result['username'],
                'user_id': result['user_id'],
                'avatarUrl': result['avatarUrl'],
                'key': result['password']
            }
        })
    except Exception as e:
        print e
        return RecordLog(request.url, e)


@route_user.route('/Logout', methods=['GET'])
def Logout():
    session.pop('User')
    return ResultDeal()


@route_user.route('/CreateUser', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateUser():
    params = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'nickname': request.form.get('nickname', ''),
        'sex': request.form.get('sex', 1),
        'role_id': request.form.get('role_id', 1),
        'avatarUrl': request.form.get('avatarUrl', '')
    }

    result = UserModel().CreateUserRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_user.route('/LockUser', methods=['POST'])
@auth.login_required
@validate_current_access
def LockUser():
    result = UserModel().LockUserRequest(user_id=request.form.getlist('user_id'))
    return ResultDeal(data=result)


@route_user.route('/ModifyUser', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyUser():
    params = request.form
    Int = ['sex', 'role_id']
    for i in params:
        if i in Int:
            params[i] = int(params[i])

    result = UserModel().ModifyUserRequest(user_id=request.form.get('user_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_user.route('/QueryUserByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryUserByParam():
    params = request.form
    Int = ['sex', 'role_id']
    Bool = ['isLock']
    for i in params:
        if i in Int:
            params[i] = int(params[i])
        if i in Bool:
            params[i] = True if params[i] == 'true' else False

    result = UserModel().QueryUserByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
