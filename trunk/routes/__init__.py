# -*- coding:UTF-8 -*-
# trunk/routes/__init__.py
from .v1.user import route_user


def init_app(app):
    app.register_blueprint(route_user)
