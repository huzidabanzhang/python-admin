# -*- coding:UTF-8 -*-
# trunk/models/User.py
from models.base import db
import datetime


class User(db.Model):
    '''
    用户
    '''
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(64))
    sex = db.Column(db.SmallInteger, default=1)
    role_id = db.Column(db.Integer, db.ForeignKey('db_role.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)
    __table_args__ = ({"useexisting": True})

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % self.username


MenuToRole = db.Table(
    'db_menu_to_role',
    db.Column('role_id', db.Integer, db.ForeignKey('db_role.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('db_menu.id'))
)


RouteToRole = db.Table(
    'db_route_to_role',
    db.Column('route_id', db.Integer, db.ForeignKey('db_route.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('db_menu.id'))
)


class Role(db.Model):
    '''
    权限
    '''
    __tablename__ = 'db_role'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    type = db.Column(db.SmallInteger, index=True, default=1)
    users = db.relationship('User', backref='role')
    menus = db.relationship('Menu',
                            secondary=MenuToRole,
                            backref=db.backref('db_role', lazy='dynamic'),
                            lazy='dynamic')
    routes = db.relationship('Route',
                             secondary=RouteToRole,
                             backref=db.backref('db_route', lazy='dynamic'),
                             lazy='dynamic')
    __table_args__ = ({"useexisting": True})

    def __repr__(self):
        return '<Role %r>' % self.name


class Route(db.Model):
    '''
    路由
    '''
    __tablename__ = 'db_route'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    permission = db.Column(db.SmallInteger, index=True, default=1)
    description = db.Column(db.String(255), nullable=False)
    isLock = db.Column(db.Boolean, index=True, default=True)
    __table_args__ = ({"useexisting": True})

    def __repr__(self):
        return '<Route %r>' % self.name


class Menu(db.Model):
    '''
    菜单
    '''
    __tablename__ = 'db_menu'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    parentId = db.Column(db.Integer, nullable=False, index=True, default=0)
    title = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    sort = db.Column(db.SmallInteger, index=True, default=1)
    permission = db.Column(db.SmallInteger, index=True, default=1)
    isLock = db.Column(db.Boolean, index=True, default=True)
    routes = db.relationship('Route', backref='menu')
    __table_args__ = ({"useexisting": True})

    def __repr__(self):
        return '<Menu %r>' % self.title
