#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: API蓝图初始化注册
@Author: Zpp
@Date: 2019-09-04 10:23:46
LastEditTime: 2022-04-29 10:02:58
LastEditors: Zpp
'''
from .v1.admin import route_admin
from .v1.menu import route_menu
from .v1.role import route_role
from .v1.interface import route_interface
from .v1.document import route_document
from .v1.folder import route_folder
from .v1.log import route_log
from .v1.base import route_base

from flask import current_app, session, make_response, request
from libs.code import ResultDeal, GetTimestamp
from models import db
from models.system import InitSql
from datetime import datetime
from libs.utils import health_database_status
from healthcheck import HealthCheck


def init_app(app):
    health = HealthCheck(app, "/healthcheck")

    @app.before_first_request
    def before_first_request():
        session['requestTime'] = GetTimestamp()

        # 运行检查是否连接数据库
        s = db.session()
        if health.add_check(health_database_status(s, 'SELECT 1')):
            # 检查是否存在数据表
            if health.add_check(health_database_status(s, 'SELECT * FROM db_init_sql')):
                res = s.query(InitSql).first()
                if not res:
                    s.add(InitSql(is_init=False))
                    s.commit()
            else:
                # 创建数据表
                db.create_all()
        else:
            return ResultDeal(code=-1, msg='数据库未连接或者连接配置错误')

    @app.before_request
    def handel_before_request():
        session['requestTime'] = GetTimestamp()

    @app.teardown_request
    def handel_teardown_request(response):
        if response:
            db.session.close()

    @app.errorhandler(401)
    def handle_401_error(error):
        return '登录认证失效，请重新登录', 401

    @app.errorhandler(403)
    def handle_403_error(error):
        return '您没有访问权限', 403

    @app.errorhandler(404)
    def handle_404_error(error):
        return '文件或者页面不存在', 404

    @app.errorhandler(405)
    def handle_404_error(error):
        return '方法不被允许', 405

    @app.errorhandler(500)
    def handle_500_error(error):
        return '服务器错误 % s' % error, 500

    @app.route('/favicon.ico')
    def favicon():
        return current_app.send_static_file('favicon.ico')

    routes = [
        route_admin,
        route_menu,
        route_role,
        route_interface,
        route_document,
        route_folder,
        route_log,
        route_base
    ]

    for r in routes:
        app.register_blueprint(r)
