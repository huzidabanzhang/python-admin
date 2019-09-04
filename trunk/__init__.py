# -*- coding:UTF-8 -*-
# trunk/__init__.py
from flask import Flask
import services


def create_app():
    app = Flask(__name__)
    # models.init_app(app)
    # routes.init_app(app)
    services.init_app(app)
    return app

create_app().run()
