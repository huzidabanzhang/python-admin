#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 16:06:14
@LastEditTime: 2019-10-15 10:59:49
@LastEditors: Zpp
'''

from flask import current_app, request, session, abort
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from libs.error_code import ResultDeal
from libs.scope import is_in_scope

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, pwd):
    # token
    # HTTP 账号密码
    # header key:value
    # account  账号
    # 密码
    # key=随机
    # value =basic base64(账号:密码)
    if not token:
        return False

    user_info = verify_auth_token(token, pwd)
    if not user_info:
        return False
    else:
        return True


@auth.error_handler
def unauthorized():
    abort(401)


def generate_auth_token(params, expiration=24 * 3600):
    """
    生成token
    params 参数
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps(params)


def verify_auth_token(token, pwd):
    info = session.get('User')
    if not info or info != token:
        return False

    data = get_auth_token(token)
    return data if data.get('password') == pwd else False


def get_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False

    return data


def validate_current_access(f):
    @wraps(f)
    def decorated_function(*args, **kws):
         # 路由权限
        info = get_auth_token(session.get('User'))
        if info['is_admin']:
            return f(*args, **kws)
        
        allow = is_in_scope(info['user_id'], request.path)
        if not allow:
            abort(403)

        return f(*args, **kws)

    return decorated_function
