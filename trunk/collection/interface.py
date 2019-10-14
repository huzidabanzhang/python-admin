#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口控制器
@Author: Zpp
@Date: 2019-10-14 13:40:29
@LastEditors: Zpp
@LastEditTime: 2019-10-14 14:58:13
'''
from flask import request
from models.base import db
from models.system import Interface
from libs.error_code import RecordLog
import uuid


class InterfaceModel():
    def QueryInterfaceByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        接口列表
        '''
        s = db.session()
        try:
            Int = ['menu_id', 'isLock', 'method']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Interface.query.filter_by(*data).filter(
                Interface.name.like("%" + params['name'] + "%") if params.has_key('name') else ''
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

    def CreateInterfaceRequest(self, params):
        '''
        新建接口
        '''
        s = db.session()
        try:
            item = Interface(
                interface_id=uuid.uuid4,
                name=params['name'],
                path=params['path'],
                method=params['method'],
                description=params['description'],
                menu_id=params['menu_id']
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

    def GetInterfaceRequest(self, interface_id):
        '''
        查询接口
        '''
        s = db.session()
        try:
            interface = s.query(Interface).filter(Interface.interface_id == interface_id).first()
            if not interface:
                return str('接口不存在')

            return interface.to_json()
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def ModifyInterfaceRequest(self, interface_id, params):
        '''
        修改接口信息
        '''
        s = db.session()
        try:
            interface = s.query(Interface).filter(Interface.interface_id == interface_id).first()
            if not interface:
                return str('接口不存在')

            AllowableFields = ['name', 'path', 'method', 'description', 'menu_id']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Interface).filter(Interface.interface_id == interface_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()

    def LockInterfaceRequest(self, interface_id):
        '''
        禁用接口
        '''
        s = db.session()
        try:
            for key in interface_id:
                interface = s.query(Interface).filter(Interface.interface_id == key).first()
                if not interface:
                    continue
                interface.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()
