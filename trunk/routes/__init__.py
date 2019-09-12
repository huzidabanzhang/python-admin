#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-04 10:23:46
@LastEditTime: 2019-09-12 11:28:56
@LastEditors: Zpp
'''
from .v1.user import route_user
from .v1.menu import route_menu
from .v1.route import route_route


def init_app(app):
    app.register_blueprint(route_user)
    app.register_blueprint(route_menu)
    app.register_blueprint(route_route)
