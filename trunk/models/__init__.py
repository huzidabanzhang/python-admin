# -*- coding:UTF-8 -*-
# trunk/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
from conf.setting import Config


class Pool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(Pool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        if options.has_key('pool_size'):
            del options['pool_size']

db = None

def init_app(app):
    # mysql 数据库连接数据
    app.config['SQLALCHEMY_DATABASE_URI'] = Config().get_sql_url()
    # 禁用追踪对象的修改并且发送信号（会需要额外内存）
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    global db
    db = Pool_SQLAlchemy(app)
