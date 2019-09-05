# -*- coding:UTF-8 -*-
# trunk/routes/token_auth.py

from flask import current_app, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from libs.error_code import AuthFailed, Forbidden
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
    user_info = verify_auth_token(token, pwd)
    if not user_info:
        return False
    else:
        return True


def generate_auth_token(params, expiration=30 * 24 * 3600):
    """
    生成token
    params 参数
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps(params)


def verify_auth_token(token, pwd):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        raise AuthFailed(msg='token已过期', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token不合法', error_code=1002)

    if data.get(data.get('user_name')) != pwd:
        return False

    # 路由权限
    allow = is_in_scope(data['scope'], request.endpoint)
    if not allow:
        raise Forbidden()
    return data
