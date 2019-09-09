# -*- coding:UTF-8 -*-
# trunk/models/base.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool


class Pool_SQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(Pool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        if options.has_key('pool_size'):
            del options['pool_size']


db = Pool_SQLAlchemy()
