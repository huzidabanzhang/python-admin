#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 路由控制器
@Author: Zpp
@Date: 2019-09-10 16:00:22
@LastEditTime : 2020-02-14 14:20:01
@LastEditors  : Please set LastEditors
'''
from flask import request
from models.base import db
from models.system import Route
from sqlalchemy import text
import uuid


class RouteModel():
    def QueryRouteByParamRequest(self, params):
        '''
        路由列表
        '''
        s = db.session()
        try:
            data = {}
            if params.has_key('is_disabled'):
                data['is_disabled'] = params['is_disabled']

            result = Route.query.filter_by(**data).filter(
                Route.name.like("%" + params['name'] + "%") if params.has_key('name') else text('')
            ).order_by(Route.id).all()

            return [value.to_json() for value in result]
        except Exception as e:
            print e
            return str(e.message)

    def CreateRouteRequest(self, params):
        '''
        新建路由
        '''
        s = db.session()
        try:
            item = Route(
                route_id=uuid.uuid4(),
                pid=params['pid'],
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
            return str(e.message)

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
            return str(e.message)

    def ModifyRouteRequest(self, route_id, params):
        '''
        修改路由信息
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id == route_id).first()
            if not route:
                return str('路由不存在')

            AllowableFields = ['pid', 'name', 'path', 'title', 'component', 'componentPath', 'cache']
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
            return str(e.message)

    def LockRouteRequest(self, route_id, is_disabled):
        '''
        禁用路由
        '''
        s = db.session()
        try:
            s.query(Route).filter(Route.route_id.in_(route_id)).update({Route.is_disabled: is_disabled})
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelRouteRequest(self, route_id):
        '''
        删除路由
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id == route_id).first()
            s.delete(route)

            # 子菜单移动到根目录
            s.query(Route).filter(Route.pid == route_id).update({
                'pid': '0'
            })
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
