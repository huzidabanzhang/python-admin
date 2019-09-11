# -*- coding:UTF-8 -*-
# trunk/routes/__init__.py
from .v1.user import route_user
from .v1.menu import route_menu
from .v1.route import route_route


def init_app(app):
    app.register_blueprint(route_user)
    app.register_blueprint(route_menu)
    app.register_blueprint(route_route)
