#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 路由控制器
@Author: Zpp
@Date: 2019-09-10 16:00:22
@LastEditTime: 2019-10-15 15:37:20
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import Route
from libs.error_code import RecordLog
import uuid


class RouteModel():
    def QueryRouteByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        路由列表
        '''
        s = db.session()
        try:
            Int = ['menu_id', 'isLock']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Route.query.filter_by(*data).filter(
                Route.name.like("%" + params['name'] + "%") if params.has_key('name') else ''
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def CreateRouteRequest(self, params):
        '''
        新建路由
        '''
        s = db.session()
        try:
            item = Route(
                route_id=uuid.uuid4,
                parentId=params['parentId'],
                name=params['name'],
                title=params['title'],
                path=params['path'],
                component=params['component'],
                componentPath=params['componentPath'],
                cache=params['cache']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def GetRouteRequest(self, route_id):
        '''
        查询路由
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id == route_id).first()
            if not route:
                return str('路由不存在')

            return route.to_json()
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def ModifyRouteRequest(self, route_id, params):
        '''
        修改路由信息
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id == route_id).first()
            if not route:
                return str('路由不存在')

            AllowableFields = ['parentId', 'name', 'path', 'title', 'component', 'componentPath', 'cache']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Route).filter(Route.route_id == route_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()

    def LockRouteRequest(self, route_id):
        '''
        禁用路由
        '''
        s = db.session()
        try:
            for key in route_id:
                route = s.query(Route).filter(Route.route_id == key).first()
                if not route:
                    continue
                route.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()
