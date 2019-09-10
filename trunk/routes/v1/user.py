# -*- coding:UTF-8 -*-
# trunk/routes/v1/user.py
from flask import Blueprint, request
from collection.user import UserModel
from ..token_auth import auth, generate_auth_token
from libs.error_code import ResultDeal

route_user = Blueprint('User', __name__, url_prefix='/User')


@route_user.route('/CreateDrop', methods=['POST'])
def CreateDrop():
    result = UserModel().CreateDropRequest()
    return ResultDeal(msg=True)


@route_user.route('/Login', methods=['POST'])
def Login():
    result = UserModel().GetUserRequest(
        username=request.form.get('username'),
        password=request.form.get('password')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    token = generate_auth_token({
        'username': result.username,
        'user_id': result.user_id,
        'role_id': result.role_id,
        'password': result.password,
        'nickname': result.nickname
    })

    return ResultDeal(data=token)


@route_user.route('/CreateUser', methods=['POST'])
@auth.login_required
def CreateUser():
    params = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'nickname': request.form.get('nickname') or '',
        'sex': request.form.get('sex') or 1,
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
