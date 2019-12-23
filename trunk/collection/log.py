#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志控制器
@Author: Zpp
@Date: 2019-10-17 14:53:00
@LastEditors  : Zpp
@LastEditTime : 2019-12-23 15:50:15
'''
from flask import request
from models.base import db
from models.log import Log
from sqlalchemy import text
import json


class LogModel():
    def QueryLogByParamRequest(self, params, page=1, page_size=20):
        '''
        日志列表
        '''
        s = db.session()
        try:
            filters = {
                Log.type.in_(params['type']) if params.has_key('type') else text('1 = 1'),
                Log.status.in_(params['status']) if params.has_key('status') else text('1 = 1')
            }
            
            result = Log.query.filter(*filters).order_by(text('-id')).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)

    def CreateLogRequest(self, params):
        '''
        新建日志
        '''
        try:
            s = db.session()
            if not params['username']:
                return True

            type = 0
            if params['path'] == '/v1/Admin/Login':
                type = 1
                if str(params['content']) == '管理员被禁用':
                    params['status'] = 2

            item = Log(
                ip=params['ip'],
                method=params['method'],
                path=params['path'],
                username=params['username'],
                status=params['status'],
                time=params['time'],
                content=str(params['content']),
                params=json.dumps(params['params']),
                type=type
            )
            s.add(item)
            s.commit()
            return True
        except Exception, e:
            print e
            return False
