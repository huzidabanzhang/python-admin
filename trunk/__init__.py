# -*- coding:UTF-8 -*-
# trunk/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
import services, models


class Pool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(Pool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        if options.has_key('pool_size'):
            del options['pool_size']


def create_app():
    app = Flask(__name__)
    models.init_app(app)
    # routes.init_app(app)
    services.init_app(app)
    return app


app = create_app()

# sql
db = Pool_SQLAlchemy(app)
# 启动
app.run()