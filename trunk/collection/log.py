#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志控制器
@Author: Zpp
@Date: 2019-10-17 14:53:00
@LastEditors: Zpp
@LastEditTime: 2019-10-18 10:34:09
'''
from flask import request
from models.base import db
from models.log import Log


class LogModel():
    def QueryLogByParamRequest(self, params, page=1, page_size=20):
        '''
        日志列表
        '''
        s = db.session()
        try:
            Int = ['status', 'type']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Log.query.filter_by(*data).order_by('-id').paginate(page, page_size, error_out=False)

            data = []
            for value in result:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
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
                if params['content'] == '管理员被禁用':
                    params['status'] = 2

            item = Log(
                ip=params['ip'],
                method=params['method'],
                path=params['path'],
                username=params['username'],
                status=params['status'],
                time=params['time'],
                content=str(params['content']),
                params=str(params['params']),
                type=type
            )
            s.add(item)
            s.commit()
            return True
        except Exception, e:
            print e
            return False
