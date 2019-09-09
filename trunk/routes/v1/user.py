# -*- coding:UTF-8 -*-
# trunk/routes/v1/user.py
from flask import Blueprint, request, jsonify
from collection.user import UserModel

route_user = Blueprint('User', __name__, url_prefix='/User')


@route_user.route('/CreateDrop', methods=['POST'])
def CreateDrop():
    result = UserModel().CreateDropRequest()
    return jsonify({'msg': True})


@route_user.route('/QueryUserByParam', methods=['POST'])
def QueryUserByParam():
    result = UserModel().QueryUserByParamRequest()
    return jsonify({'data': result})
