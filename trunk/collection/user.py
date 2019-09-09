# -*- coding:UTF-8 -*-
# trunk/collection/user.py
from models.base import db
from models.user import User


class UserModel():
    def QueryUserByParamRequest(self):
        try:
            s = db.session()
            result = s.query(User).all()
            s.close()
            return result
        except Exception as e:
            print e
            return False
