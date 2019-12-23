#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹控制器
@Author: Zpp
@Date: 2019-12-23 14:53:50
@LastEditors  : Zpp
@LastEditTime : 2019-12-23 15:45:07
'''
from flask import request
from models.base import db
from models.system import Folder
from sqlalchemy import text
import uuid


class FolderModel():
    def QueryFolderByParamRequest(self, params):
        '''
        文件夹列表
        '''
        s = db.session()
        try:
            result = Folder.query.order_by(Folder.id).all()

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
                parent_id=params['parent_id'],
                name=params['name']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetFolderRequest(self, folder_id):
        '''
        查询文件夹下文档
        '''
        s = db.session()
        try:
            folder = s.query(Folder).filter(Folder.folder_id == folder_id).first()
            if not folder:
                return str('文件夹不存在')

            return [value.to_json() for value in folder.documents]
        except Exception as e:
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
            folder.parent_id = params['parent_id']
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelFolderRequest(self, folder_id, isFolder=True):
        '''
        删除文件夹
        isFolder True：删除关联文件夹 False：关联文件夹移到根目录
        关联文档默认到根目录
        '''
        s = db.session()
        try:
            folder = s.query(Folder).filter(Folder.folder_id == folder_id).first()
            if not folder:
                return str('文件夹不存在')

            folder_list = s.query(Folder).filter(Folder.parent_id == folder_id).all()
            if not isFolder:
                for i in folder_list:
                    s.query(Document).filter(Document.folder_id == i.folder_id).update({Document.folder_id: '0'})
                folder_list.update({Folder.parent_id: '0'})
            else:
                folder_list.delete()

            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
