# -*- coding:UTF-8 -*-
# trunk/app.py
from flask import Flask
import models
import routes
import services


def create_app():
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app


# 初始化
app = create_app()
# print app.url_map
app.run()
