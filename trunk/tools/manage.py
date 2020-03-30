#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 数据库迁移
@Author: Zpp
@Date: 2020-03-30 11:01:56
@LastEditors: Zpp
@LastEditTime: 2020-03-30 11:15:09
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

# 初始化 migrate
# 两个参数一个是 Flask 的 app，一个是数据库 db
migrate = Migrate(app, db)

# 初始化管理器
manager = Manager(app)
# 添加 db 命令，并与 MigrateCommand 绑定
manager.add_command('db', MigrateCommand)


class User(db.Model):
    '''
    构建我们的数据模型
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


if __name__ == '__main__':
    manager.run()
