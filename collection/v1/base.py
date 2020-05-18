#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2020-02-19 19:45:33
@LastEditTime: 2020-05-18 10:41:41
@LastEditors: Zpp
'''
from models import db
from models.system import Admin, Role, Menu, Interface, InitSql, Folder
from models.log import Log
from .interface import InterfaceModel
from .menu import MenuModel
from conf.setting import _config, init_menu, sql_dir, GeoLite2_dir, default
from sqlalchemy import func, desc
import geoip2.database
import uuid
import datetime
import random
import copy
import os
import time


class BaseModel():
    def __init__(self):
        self.role_name = u'超级管理员'
        self.user_name = u'Admin'
        self.M = MenuModel()
        self.I = InterfaceModel()

    def CreateDropRequest(self, isInit, params=None):
        db.session.remove()
        db.drop_all()
        db.create_all()

        s = db.session()
        try:
            s.add(InitSql(isInit=False))
            s.commit()

            role_id = uuid.uuid4()
            role = Role(
                role_id=role_id,
                name=self.role_name,
                mark=default['role_mark']
            )
            s.add(role)
            s.commit()

            password = self.__get_code()
            if not isInit:
                admin = Admin(
                    admin_id=uuid.uuid4(),
                    username=self.user_name,
                    password=_config.get_md5(password),
                    avatarUrl='',
                    role_id=role_id
                )
            else:
                admin = Admin(
                    admin_id=params['admin_id'],
                    username=self.user_name,
                    password=params['password'],
                    avatarUrl='',
                    role_id=role_id
                )
            s.add(admin)
            s.commit()

            self.__init_menus(s, init_menu)

            folder = Folder(
                folder_id=uuid.uuid4(),
                admin_id=None,
                name=u'系统文件',
                is_sys=True
            )
            s.add(folder)
            s.commit()

            sql = s.query(InitSql).one()
            sql.isInit = True
            s.commit()
            return {
                'username': 'Admin',
                'password': password
            }
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def __get_code(self):
        code_list = []
        for i in range(10):   # 0~9
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
        code = random.sample(code_list, 6)  # 随机取6位数
        code_num = ''.join(code)
        return code_num

    def __init_menus(self, s, data, pid='0'):
        for m in data:
            menu_id = uuid.uuid4()
            is_exists = self.M.isCreateExists(s, m)

            if is_exists == True:
                menu = self.__create_menu(m, menu_id, pid)
                s.add(menu)
            else:
                menu = is_exists['value']

            if m.has_key('interface'):
                interfaces = []
                for f in m['interface']:
                    is_exists = self.I.isCreateExists(s, f)
                    if is_exists == True:
                        interface = self.__create_interface(s, f, uuid.uuid4())
                    else:
                        interface = is_exists['value']
                    s.add(interface)
                    interfaces.append(interface)
                menu.interfaces = interfaces

            s.commit()
            if m.has_key('children'):
                self.__init_menus(s, m['children'], menu_id)

    def __create_menu(self, params, menu_id, pid):
        return Menu(
            menu_id=menu_id,
            pid=pid,
            title=params['title'],
            path=params['path'],
            icon=params['icon'],
            mark=params['mark'],
            component=params['component'],
            componentPath=params['componentPath'],
            name=params['name'],
            cache=params['cache']
        )

    def __create_interface(self, s, params, interface_id):
        return Interface(
            interface_id=interface_id,
            name=params['name'],
            path=params['path'],
            method=params['method'],
            description=params['description'],
            mark=params['mark'],
            forbidden=params['forbidden']
        )

    def ExportSql(self, type=1):
        try:
            if not os.path.exists(sql_dir):
                os.mkdir(sql_dir)

            os.chdir(sql_dir)
            filename = 'TABLE%s.sql' % int(time.time() * 1000)

            sqlfromat = "%s -h%s -u%s -p%s -P%s %s >%s"
            if type == 2:
                sqlfromat = "%s -h%s -u%s -p%s -P%s -d %s >%s"  # 不包含数据
            if type == 3:
                sqlfromat = "%s -h%s -u%s -p%s -P%s -t %s >%s"  # 不包含表结构

            sql = (sqlfromat % ('mysqldump ',
                                _config.host,
                                _config.admin,
                                _config.password,
                                _config.port,
                                _config.db,
                                filename))
            os.system(sql)
            return {
                'path': os.path.join(sql_dir, filename),
                'name': filename
            }
        except Exception as e:
            print e
            return str(e.message)

    def ImportSql(self, file):
        s = db.session()
        try:
            filename = 'TABLE%s.sql' % int(time.time() * 1000)
            config = _config

            if not os.path.exists(sql_dir):
                os.mkdir(sql_dir)

            file_path = os.path.join(sql_dir, filename)
            file.save(file_path)

            sqlfromat = "%s -h%s -u%s -p%s -P%s %s <%s"
            sql = (sqlfromat % ('mysql ',
                                _config.host,
                                _config.admin,
                                _config.password,
                                _config.port,
                                _config.db,
                                file_path))

            db.drop_all()
            os.system(sql)
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetLoginInfo(self, username):
        '''
        获取用户登录情况
        '''
        s = db.session()
        try:
            params = {
                'username': username,
                'type': 1
            }

            user_time = s.query(
                func.count(Log.username),
                func.date_format(Log.create_time, '%Y-%m-%d').label('date')
            ).filter_by(**params).group_by('date').all()

            last_time = s.query(
                func.date_format(Log.create_time, '%Y-%m-%d %H:%m:%S')
            ).filter_by(**params).order_by(desc('id')).first()

            role_info = s.query(
                Role.name,
                Role.mark,
                Admin.avatarUrl
            ).filter(
                Admin.username == username,
                Admin.role_id == Role.role_id
            ).first()

            data = []
            for i in user_time:
                data.append({
                    u'日期': i[1],
                    username: i[0]
                })

            return {
                'rows': data,
                'columns': [u'日期', username],
                'info': {
                    'time': last_time[0],
                    'role_name': role_info[0],
                    'mark': role_info[1],
                    'avatarUrl': role_info[2],
                    'isAdmin': role_info[1] == default['role_mark']
                }
            }
        except Exception as e:
            print e
            return str(e.message)

    def GetAllUserLoginCount(self):
        '''
        获取所有用户登录次数
        '''
        s = db.session()
        try:
            user_count = s.query(
                Log.username,
                func.count(Log.username)
            ).filter(
                Log.type == 1
            ).group_by('username').all()

            user_list = [u'用户', u'登录次数']
            data = []
            for i in user_count:
                user_list.append(i[0])
                data.append({
                    u'用户': i[0],
                    u'登录次数': i[1]
                })

            return {
                'data': data,
                'user': user_list
            }
        except Exception as e:
            print e
            return str(e.message)

    def GetUserLoginIp(self):
        '''
        获取用户登录IP分布情况
        '''
        s = db.session()
        try:
            params = {
                'type': 1
            }

            ip_list = s.query(
                Log.ip
            ).filter_by(**params).group_by('ip').all()

            reader = geoip2.database.Reader(GeoLite2_dir)

            ip = {}
            city = {}
            for i in ip_list:
                try:
                    response = reader.city(i[0])
                    if not ip.has_key(response.city.names["zh-CN"]):
                        ip[response.city.names["zh-CN"]] = {
                            'count': 1,
                            'ip': [i[0]]
                        }
                    else:
                        ip[response.city.names["zh-CN"]]['count'] += 1
                        ip[response.city.names["zh-CN"]]['ip'].append(i[0])

                    city[response.city.names["zh-CN"]] = [
                        response.location.longitude,
                        response.location.latitude
                    ]
                except:
                    continue

            return {
                'ip': ip,
                'city': city
            }
        except Exception as e:
            print e
            return str(e.message)
