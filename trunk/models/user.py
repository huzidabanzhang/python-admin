# -*- coding:UTF-8 -*-
# trunk/models/User.py
from app import db
import datetime


class User(db.Model):
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(64))
    sex = db.Column(db.INT(), default=1)
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now)
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
