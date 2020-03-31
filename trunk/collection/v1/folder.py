#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹控制器
@Author: Zpp
@Date: 2019-12-23 14:53:50
@LastEditors  : Please set LastEditors
@LastEditTime : 2020-02-14 14:49:46
'''
from flask import request
from models import db
from models.system import Folder, Document
from sqlalchemy import text, or_, and_
import uuid


class FolderModel():
    def QueryFolderByParamRequest(self, pid, admin_id):
        '''
        文件夹列表
        '''
        s = db.session()
        try:
            result = Folder.query.filter(
                or_(
                    and_(
                        Folder.is_sys == True,
                        Folder.pid == pid,
                    ),
                    and_(
                        Folder.is_sys == False,
                        Folder.pid == pid,
                        Folder.admin_id == admin_id
                    )
                )
            ).order_by(Folder.id).all()

            return [value.to_json() for value in result]
        except Exception as e:
            print e
            return str(e.message)

    def CreateFolderRequest(self, params):
        '''
        新建文件夹
        '''
        s = db.session()
        try:
            item = Folder(
                folder_id=uuid.uuid4(),
                pid=params['pid'],
                name=params['name'],
                admin_id=params['admin_id'],
                is_sys=params['is_sys']
            )
            s.add(item)
            s.commit()
            return item.to_json()
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def ModifyFolderRequest(self, folder_id, params):
        '''
        修改文件夹
        '''
        s = db.session()
        try:
            folder = s.query(Folder).filter(Folder.folder_id == folder_id).first()
            if not folder:
                return str('文件夹不存在')

            folder.name = params['name']
            if params.has_key('pid'):
                folder.pid = params['pid']
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelFolderRequest(self, folder_id):
        '''
        删除文件夹
        关联文档默认到根目录
        '''
        s = db.session()
        try:
            folder = s.query(Folder).filter(Folder.folder_id == folder_id).first()
            if not folder:
                return str('文件夹不存在')

            res = s.query(Folder).filter(Folder.pid == folder_id).all()
            for i in res:
                i.pid = '0'

            s.delete(folder)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
