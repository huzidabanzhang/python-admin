#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: API蓝图初始化注册
@Author: Zpp
@Date: 2019-09-04 10:23:46
@LastEditTime: 2019-10-17 16:59:04
@LastEditors: Zpp
'''
from .v1.admin import route_admin
from .v1.menu import route_menu
from .v1.route import route_route
from .v1.role import route_role
from .v1.interface import route_interface
from .v1.document import route_document
from .v1.log import route_log

from flask import request, current_app, session
from libs.code import ResultDeal
from collection.log import LogModel
from datetime import datetime
from models.base import db
import json


def init_app(app):
    @app.before_request
    def handel_before_request():
        session['requestTime'] = datetime.now()


    @app.after_request
    def handel_after_request(response):
        if response.headers['Content-Type'] == 'application/json' and response.status_code == 200:
            params = {
                'ip': request.remote_addr,
                'method': request.method,
                'path': request.path,
                'username': session.get('username'),
                'time': (datetime.now() - session.get('requestTime')).seconds * 1000
            }
            print request.path
            print response.get_data()
            # body = json.loads(response.data)
            # print body
            # print body['data']
            # if body['code'] == 0:
            #     params['status'] = 0
            #     params['content'] = json.dumps(body['data'])
            #     LogModel().CreateLogRequest(params)
            # if body['code'] == -1:
            #     params['status'] = 1
            #     params['content'] = body['msg']
            #     LogModel().CreateLogRequest(params)

        return response


    @app.teardown_request
    def handel_teardown_request(response):
        if response:
            db.session.close()


    @app.errorhandler(401)
    def handle_401_error(error):
        return ResultDeal(code=401, msg=u'登录认证失效，请重新登录')


    @app.errorhandler(403)
    def handle_403_error(error):
        return ResultDeal(code=403, msg=u'您没有访问权限')


    @app.errorhandler(404)
    def handle_404_error(error):
        return ResultDeal(code=404, msg=u'页面不存在')


    @app.errorhandler(405)
    def handle_404_error(error):
        return ResultDeal(code=405, msg=u'方法不被允许')


    @app.errorhandler(500)
    def handle_500_error(error):
        return ResultDeal(code=500, msg=u'服务器错误 %s' % error)


    @app.route('/favicon.ico')
    def favicon():
        return current_app.send_static_file('favicon.ico')

    app.register_blueprint(route_admin)
    app.register_blueprint(route_menu)
    app.register_blueprint(route_route)
    app.register_blueprint(route_role)
    app.register_blueprint(route_interface)
    app.register_blueprint(route_document)
    app.register_blueprint(route_log)
