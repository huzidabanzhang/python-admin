#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 数据库API
@Author: Zpp
@Date: 2020-02-21 13:02:28
@LastEditTime: 2020-05-28 13:53:18
@LastEditors: Zpp
'''
from flask import Blueprint, request, make_response, session, abort
from collection.v1.base import BaseModel
from ..token_auth import auth, generate_auth_token, validate_current_access, get_auth_token
from libs.code import ResultDeal
from libs.utils import readFile
from validate import validate_form
from validate.v1.base import params
import json
import os

route_base = Blueprint('Base', __name__, url_prefix='/v1/Base')
validate = validate_form(params)


@route_base.route('/CreateDrop', methods=['GET'])
def CreateDrop():
    result = BaseModel().CreateDropRequest(False)
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_base.route('/AgainCreateDrop', methods=['GET'])
@auth.login_required
@validate_current_access
def AgainCreateDrop():
    result = BaseModel().CreateDropRequest(True, get_auth_token(session.get('admin')))
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_base.route('/ExportSql', methods=['POST'], endpoint='ExportSql')
@auth.login_required
@validate_current_access
@validate.form('Export')
def ExportSql():
    result = BaseModel().ExportSql(int(request.form.get('type')))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    if os.path.exists(result['path']):
        res = make_response(readFile(result['path'], 'rb'))
        res.headers['Content-Type'] = 'application/octet-stream'
        res.headers['filename'] = result['name']
        res.headers['Content-Disposition'] = 'attachment; filename=' + result['name']
        return res
    else:
        abort(404)


@route_base.route('/ImportSql', methods=['POST'], endpoint='ImportSql')
@auth.login_required
@validate_current_access
@validate.form('Import')
def ImportSql():
    result = BaseModel().ImportSql(request.files.get('document'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_base.route('/GetLoginInfo', methods=['POST'], endpoint='GetLoginInfo')
@auth.login_required
@validate_current_access
@validate.form('Login')
def GetLoginInfo():
    result = BaseModel().GetLoginInfo(
        request.form.get('admin_id'),
        request.form.get('time')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_base.route('/GetAllUserLoginCount', methods=['POST'])
@auth.login_required
@validate_current_access
def GetAllUserLoginCount():
    result = BaseModel().GetAllUserLoginCount()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_base.route('/GetUserLoginIp', methods=['POST'])
@auth.login_required
@validate_current_access
def GetUserLoginIp():
    result = BaseModel().GetUserLoginIp()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
