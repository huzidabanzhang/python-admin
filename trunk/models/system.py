#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 系统相关的几张表结构
@Author: Zpp
@Date: 2019-09-05 15:57:55
@LastEditTime : 2020-02-05 14:45:38
@LastEditors  : Please set LastEditors
'''
from models.base import db
import datetime


MenuToRole = db.Table(
    'db_menu_to_role',
    db.Column('role_id', db.String(36), db.ForeignKey('db_role.role_id')),
    db.Column('menu_id', db.String(36), db.ForeignKey('db_menu.menu_id'))
)


InterfaceToRole = db.Table(
    'db_interface_to_role',
    db.Column('role_id', db.String(36), db.ForeignKey('db_role.role_id')),
    db.Column('interface_id', db.String(36), db.ForeignKey('db_interface.interface_id'))
)


class Admin(db.Model):
    '''
    管理员
    '''
    __tablename__ = 'db_admin'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    admin_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(255))
    sex = db.Column(db.SmallInteger, default=1)
    avatarUrl = db.Column(db.String(255))
    is_disabled = db.Column(db.Boolean, index=True, default=True)
    deleted = db.Column(db.Boolean, index=True, default=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    login_ip = db.Column(db.String(255), index=True)
    login_time = db.Column(db.DateTime, index=True)
    role_id = db.Column(db.String(36), db.ForeignKey('db_role.role_id'))
    __table_args__ = ({"useexisting": True})

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.admin_id)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "update_time" in dict:
            dict["update_time"] = dict["update_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "last_login_time" in dict:
            dict["last_login_time"] = dict["last_login_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "login_time" in dict:
            dict["login_time"] = dict["login_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<admin %r>' % self.username


class Role(db.Model):
    '''
    权限
    '''
    __tablename__ = 'db_role'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    role_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    mark = db.Column(db.String(64), nullable=False, unique=True)
    is_disabled = db.Column(db.Boolean, index=True, default=True)
    admins = db.relationship('Admin', backref='role')
    menus = db.relationship('Menu',
                            secondary=MenuToRole,
                            backref=db.backref('db_role', lazy='dynamic'),
                            lazy='dynamic')
    interfaces = db.relationship('Interface',
                                 secondary=InterfaceToRole,
                                 backref=db.backref('db_interface', lazy='dynamic'),
                                 lazy='dynamic')
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Role %r>' % self.name


class Route(db.Model):
    '''
    路由
    '''
    __tablename__ = 'db_route'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    route_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    pid = db.Column(db.String(36), nullable=False, index=True, default='0')
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False, unique=True)
    component = db.Column(db.String(255), nullable=False)
    componentPath = db.Column(db.String(255), nullable=False)
    cache = db.Column(db.Boolean, index=True, default=True)
    is_disabled = db.Column(db.Boolean, index=True, default=True)
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Route %r>' % self.name


class Menu(db.Model):
    '''
    菜单
    '''
    __tablename__ = 'db_menu'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    menu_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    pid = db.Column(db.String(36), nullable=False, index=True, default='0')
    name = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    icon = db.Column(db.String(255), nullable=False)
    sort = db.Column(db.SmallInteger, index=True, default=1)
    is_disabled = db.Column(db.Boolean, index=True, default=True)
    interfaces = db.relationship('Interface', backref='menu')
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Menu %r>' % self.title


class Interface(db.Model):
    '''
    接口
    '''
    __tablename__ = 'db_interface'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    interface_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    method = db.Column(db.String(36), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    mark = db.Column(db.String(255), nullable=False, unique=True)
    is_disabled = db.Column(db.Boolean, index=True, default=True)
    menu_id = db.Column(db.String(36), db.ForeignKey('db_menu.menu_id'))
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Interface %r>' % self.name


class Document(db.Model):
    '''
    附件
    '''
    __tablename__ = 'db_document'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    document_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    admin_id = db.Column(db.String(36), index=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.SmallInteger, index=True, default=1)  # 1=图片 2=附件 （其他的自己定义了）
    ext = db.Column(db.String(64), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, index=True, default=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    folder_id = db.Column(db.String(36), db.ForeignKey('db_folder.folder_id'))
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Document %r>' % self.name


class Folder(db.Model):
    '''
    文件夹
    '''
    __tablename__ = 'db_folder'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    folder_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    pid = db.Column(db.String(36), nullable=False, index=True, default='0')
    name = db.Column(db.String(36), nullable=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    documents = db.relationship('Document', backref='folder')
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<Folder %r>' % self.name


class InitSql(db.Model):
    '''
    是否已经初始化数据库
    '''
    __tablename__ = 'db_init_sql'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    isInit = db.Column(db.Boolean, index=True, default=True)
    __table_args__ = ({"useexisting": True})
