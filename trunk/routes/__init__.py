#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: API蓝图初始化注册
@Author: Zpp
@Date: 2019-09-04 10:23:46
@LastEditTime: 2019-09-12 14:08:16
@LastEditors: Zpp
'''
from .v1.user import route_user
from .v1.menu import route_menu
from .v1.route import route_route
from .v1.role import route_role


def init_app(app):
    app.register_blueprint(route_user)
    app.register_blueprint(route_menu)
    app.register_blueprint(route_route)
    app.register_blueprint(route_role)
