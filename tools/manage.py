#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 数据库迁移
@Author: Zpp
@Date: 2020-03-30 11:01:56
@LastEditors: Zpp
@LastEditTime: 2020-04-28 09:55:26
'''
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from conf.setting import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config().get_sql_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models.salary import *
from models.system import *
from models.log import *

# 初始化 migrate
# 两个参数一个是 Flask 的 app，一个是数据库 db
migrate = Migrate(app, db)

# 初始化管理器
manager = Manager(app)
# 添加 db 命令，并与 MigrateCommand 绑定
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
