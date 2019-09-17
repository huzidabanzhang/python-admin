#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 
@Author: Zpp
@Date: 2019-09-10 16:05:51
@LastEditTime: 2019-09-17 10:19:24
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.user import Menu
from libs.error_code import RecordLog

class MenuModel():
    def QueryMenuByParamRequest(self, order_by='-id'):
        '''
        菜单列表
        '''
        s = db.session()
        try:
            result = Menu.query.order_by(order_by).all()

            data = []
            for value in result:
                data.append(value.to_json())

            return data
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def CreateMenuRequest(self, params):
        '''
        新建菜单
        '''
        s = db.session()
        try:
            item = Menu(
                parentId=int(params['parentId']),
                title=params['title'],
                permission=int(params['permission']),
                sort=int(params['sort']),
                path=params['path'],
                icon=params['icon']
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

    def GetMenuRequest(self, menu_id):
        '''
        查询菜单
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                return str('菜单不存在')

            return menu.to_json()
        except Exception as e:
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

    def ModifyMenuRequest(self, menu_id, params):
        '''
        修改菜单信息
        '''
        s = db.session()
        try:
            menu = s.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                return str('菜单不存在')

            AllowableFields = ['parentId', 'title', 'path', 'icon', 'sort', 'permission']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Menu).filter(Menu.id == menu_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()

    def LockMenuRequest(self, menu_id):
        '''
        禁用菜单
        '''
        s = db.session()
        try:
            for key in menu_id:
                menu = s.query(Menu).filter(Menu.menu_id == key).first()
                if not menu:
                    continue
                menu.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()
