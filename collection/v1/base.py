#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2020-02-19 19:45:33
@LastEditTime: 2020-06-08 09:55:34
@LastEditors: Zpp
'''
from models import db
from models.system import Admin, Role, Menu, Interface, InitSql, Folder
from models.log import Log
from .interface import InterfaceModel
from .menu import MenuModel
from conf.setting import _config, init_menu, sql_dir, GeoLite2_dir, default, basedir
from libs.utils import ReadFile, WriteFile
from sqlalchemy import func, desc
import geoip2.database
import uuid
import datetime
import random
import copy
import os
import time
import calendar


class BaseModel():
    def __init__(self):
        self.role_name = '超级管理员'
        self.user_name = 'Admin'
        self.M = MenuModel()
        self.I = InterfaceModel()

    def CreateDropRequest(self, is_init, params=None):
        db.session.remove()
        db.drop_all()
        db.create_all()

        s = db.session()
        try:
            s.add(InitSql(is_init=False))
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
            if not is_init:
                admin = Admin(
                    admin_id=uuid.uuid4(),
                    username=self.user_name,
                    password=_config.get_md5(password),
                    avatar='',
                    role_id=role_id
                )
            else:
                admin = Admin(
                    admin_id=params['admin_id'],
                    username=self.user_name,
                    password=params['password'],
                    avatar='',
                    role_id=role_id
                )
            s.add(admin)
            s.commit()

            self.__init_menus(s, init_menu)

            folder = Folder(
                folder_id=uuid.uuid4(),
                admin_id=None,
                name='系统文件',
                is_sys=True
            )
            s.add(folder)
            s.commit()

            sql = s.query(InitSql).one()
            sql.is_init = True
            s.commit()
            return {
                'username': 'Admin',
                'password': password
            }
        except Exception as e:
            s.rollback()
            print(e)
            return str(e)

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

            if 'interface' in m:
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
            if 'children' in m:
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
            forbid=params['forbid']
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
            print(e)
            return str(e)

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
            print(e)
            return str(e)

    def GetLoginInfo(self, admin_id, query_time):
        '''
        获取用户登录情况(根据用户名分组)
        '''
        s = db.session()
        try:
            admin = s.query(Admin).filter(Admin.admin_id == admin_id).first()
            role = admin.role

            is_admin = False
            if role and role.mark == default['role_mark']:
                is_admin = True

            params = {
                'type': 1,
                'status': 0
            }
            if not is_admin:
                params['username'] = admin.username

            query_time = datetime.datetime.strptime(query_time, '%Y-%m')
            days = calendar.monthrange(query_time.year, query_time.month)[1]

            res = s.query(
                Log.username,
                func.date_format(Log.create_time, '%Y-%m-%d').label('date'),
                func.count('date')
            ).filter(
                Log.create_time.between(
                    datetime.datetime(query_time.year, query_time.month, 1),
                    datetime.datetime(query_time.year, query_time.month, days)
                )
            ).filter_by(**params).group_by('date', 'username').all()

            data = {}
            for i in res:
                if i[1] not in data:
                    data[i[1]] = []
                data[i[1]].append({
                    'name': i[0],
                    'count': i[2]
                })

            return data
        except Exception as e:
            print(e)
            return str(e)

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
                Log.type == 1,
                Log.status == 0
            ).group_by('username').all()

            user_list = ['用户', '登录次数']
            data = []
            for i in user_count:
                user_list.append(i[0])
                data.append({
                    '用户': i[0],
                    '登录次数': i[1]
                })

            return {
                'data': data,
                'user': user_list
            }
        except Exception as e:
            print(e)
            return str(e)

    def GetUserLoginIp(self):
        '''
        获取用户登录IP分布情况
        '''
        s = db.session()
        try:
            ip_list = s.query(
                Log.ip
            ).filter(
                Log.type == 1,
                Log.status == 0
            ).group_by('ip').all()

            reader = geoip2.database.Reader(GeoLite2_dir)

            ip = {}
            city = {}
            for i in ip_list:
                try:
                    response = reader.city(i[0])
                    if response.city.names["zh-CN"] not in ip:
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
            print(e)
            return str(e)

    def GetReadmeContent(self):
        '''
        获取README.md的内容
        '''
        try:
            path = os.path.join(basedir, 'README.md')
            content = ReadFile(path)

            return {
                'content': content
            }
        except Exception as e:
            print(e)
            return str(e)
