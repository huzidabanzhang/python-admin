#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 管理员API
@Author: Zpp
@Date: 2019-09-06 14:19:29
@LastEditTime: 2020-06-05 10:24:47
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
from validate import validate_form
from validate.v1.admin import params
import json

route_admin = Blueprint('Admin', __name__, url_prefix='/v1/Admin')
validate = validate_form(params)


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


@route_admin.route('/Login', methods=['POST'], endpoint='Login')
@validate.form('Login')
def Login():
    # 验证码校验
    captcha = request.form.get('code')
    sesson_captcha = session.get('Captcha')

    if not sesson_captcha:
        return ResultDeal(msg=str('验证码已过期, 请刷新'), code=-1)

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
        user['is_admin'] = user['mark'] == default['role_mark']

        token = generate_auth_token({
            'admin_id': user['admin_id'],
            'password': user['password'],
            'is_admin': user['mark'] == default['role_mark']
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


@route_admin.route('/CreateAdmin', methods=['POST'], endpoint='CreateAdmin')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateAdmin():
    result = AdminModel().CreateAdminRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/LockAdmin', methods=['POST'], endpoint='LockAdmin')
@auth.login_required
@validate_current_access
@validate.form('Lock')
def LockAdmin():
    result = AdminModel().LockAdminRequest(
        admin_id=request.form.getlist('admin_id[]'),
        disable=request.form.get('disable')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/DelAdmin', methods=['POST'], endpoint='DelAdmin')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelAdmin():
    result = AdminModel().DelAdminRequest(request.form.getlist('admin_id[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_admin.route('/ModifyAdmin', methods=['POST'], endpoint='ModifyAdmin')
@auth.login_required
@validate_current_access
@validate.form('Modify')
def ModifyAdmin():
    result = AdminModel().ModifyAdminRequest(
        admin_id=request.form.get('admin_id'),
        params=request.form
    )

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


@route_admin.route('/QueryAdminByParam', methods=['POST'], endpoint='QueryAdminByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryAdminByParam():
    params = {}
    if request.form.get('disable') != None:
        params['disable'] = request.form.get('disable')
    if request.form.get('role_id'):
        params['role_id'] = request.form.get('role_id')

    result = AdminModel().QueryAdminByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
