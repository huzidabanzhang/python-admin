# -*- coding:UTF-8 -*-
# trunk/collection/role.py
from models.base import db
from models.user import Role


class RoleModel():
    def QueryRoleByParamRequest(self, page=1, page_size=20, order_by='-id'):
        '''
        权限列表
        '''
        s = db.session()
        try:
            result = Role.query.order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)
        finally:
            s.close()

    def CreateRoleRequest(self, params):
        '''
        新建权限
        '''
        s = db.session()
        try:
            item = Role(
                name=params['name'],
                type=int(params['type'])
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)
        finally:
            s.close()

    def GetRoleRequest(self, role_id):
        '''
        查询权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.id == role_id).first()
            if not role:
                return str('数据不存在')

            return role
        except Exception as e:
            print e
            return str(e.message)
        finally:
            s.close()

    def ModifyRoleRequest(self, role_id, name):
        '''
        修改权限信息
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.id == role_id).first()
            if not role:
                return str('数据不存在')

            role.name = name
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
        finally:
            s.close()

    def LockRoleRequest(self, role_id):
        '''
        禁用权限
        '''
        s = db.session()
        try:
            for key in role_id:
                role = s.query(Role).filter(Role.role_id == key).first()
                if not role:
                    continue
                role.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
        finally:
            s.close()

    def QueryRouteByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        权限列表
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
            return str(e.message)
        finally:
            s.close()

    def CreateRouteRequest(self, params):
        '''
        新建路由
        '''
        s = db.session()
        try:
            item = Route(
                name=params['name'],
                permission=int(params['permission']),
                menu_id=int(params['menu_id']),
                path=params['path'],
                description=params['description']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)
        finally:
            s.close()

    def GetRouteRequest(self, route_id):
        '''
        查询权限
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.id == route_id).first()
            if not route:
                return str('数据不存在')

            return route
        except Exception as e:
            print e
            return str(e.message)
        finally:
            s.close()

    def ModifyRouteRequest(self, route_id, params):
        '''
        修改路由信息
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.id == route_id).first()
            if not route:
                return str('路由不存在')

            AllowableFields = ['menu_id', 'name', 'path', 'permission', 'description']
            data = {}

            for i in params:
                if i in AllowableFields and params.has_key(i):
                    data[i] = params[i]

            s.query(Route).filter(Route.id == route_id).update(data)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
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
            return str(e.message)
        finally:
            s.close()
