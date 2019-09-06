# -*- coding:UTF-8 -*-
# trunk/routes/user.py
from flask import Blueprint, request
from models.user import User

route_user = Blueprint('User', __name__, url_prefix='/User')

@route_user.route('/QueryUserByParam', methods=['POST'])
def QueryUserByParam():
    result = User.all()
    return jsonify(result)
