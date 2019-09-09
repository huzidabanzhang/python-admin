# -*- coding:UTF-8 -*-
# trunk/collection/user.py
from models.base import db
from models.user import User
from conf.setting import Config
import uuid


class UserModel():
    def CreateDropRequest(self):
        db.drop_all()
        db.create_all()
        return True

    def QueryUserByParamRequest(self):
        try:
            s = db.session()
            result = s.query(User).all()
            s.close()
            return result
        except Exception as e:
            print e
            return str(e.message)

    def CreateUserRequest(self, params):
        '''
        新建用户
        '''
        try:
            s = db.session()

            user = s.query(User).filter(User.username == params['username']).first()

            if user:
                return str('用户已存在')

            item = User(
                user_id=uuid.uuid4(),
                username=params['username'],
                password=Config().get_md5(params['password']),
                sex=int(params['sex']),
                nickname=params['nickname']
            )
            s.add(item)
            s.commit()
            s.close()
            return True
        except Exception as e:
            print e
            return str(e.message)

    def GetUserRequest(self, username, password):
        '''
        查询用户
        '''
        try:
            s = db.session()
            user = s.query(User).filter(User.username == username, User.password == Config().get_md5(password)).first()
            s.close()
            if not user:
                return str('用户不存在')
            return user
        except Exception as e:
            print e
            return str(e.message)
