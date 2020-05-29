#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志API
@Author: Zpp
@Date: 2019-10-17 15:46:30
@LastEditors: Zpp
@LastEditTime: 2020-05-29 14:06:22
'''
from flask import Blueprint, request
from collection.v1.log import LogModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from validate import validate_form
from validate.v1.log import params

route_log = Blueprint('Log', __name__, url_prefix='/v1/Log')
validate = validate_form(params)


@route_log.route('/QueryLogByParam', methods=['POST'], endpoint='QueryLogByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryLogByParam():
    lists = [
        {'name': 'type', 'key': 'type[]'},
        {'name': 'status', 'key': 'status[]'}
    ]
    params = {}
    for i in lists:
        if request.form.getlist(i['key']):
            params[i['name']] = request.form.getlist(i['key'])

    result = LogModel().QueryLogByParamRequest(
        params=params,
        page=int(request.form.get('page', 1)),
        page_size=int(request.form.get('page_size', 20))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
