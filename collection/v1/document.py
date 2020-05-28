#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 上传控制器
@Author: Zpp
@Date: 2019-10-14 14:53:05
@LastEditors: Zpp
@LastEditTime: 2020-05-28 15:08:21
'''
from flask import request
from models import db
from models.system import Document
from conf.setting import document_dir
from sqlalchemy import text, or_
import uuid
import time
import os


class DocumentModel():
    def QueryDocumentByParamRequest(self, params, page=1, page_size=20, order_by='create_time'):
        '''
        文档列表
        '''
        s = db.session()
        try:
            deleted = Document.deleted == params['deleted']
            folder = Document.folder_id == params['folder_id']
            if params['folder_id'] == '0':
                folder = or_(
                    Document.folder_id == params['folder_id'],
                    Document.folder_id == None
                )

            status = text('')
            if params.has_key('status'):
                status = Document.status == int(params['status'])

            result = Document.query.filter(folder, deleted, status).order_by(order_by).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)

    def file_extension(self, filename):
        ary = filename.split('.')
        count = len(ary)
        return ary[count - 1] if count > 1 else ''

    def allowed_file(self, file):
        ALLOWED_EXTENSIONS = set(['gif', 'jpeg', 'jpg', 'png', 'psd', 'bmp', 'tiff', 'tif',
                                  'swc', 'iff', 'jpc', 'jp2', 'jpx', 'jb2', 'xbm', 'wbmp'])

        return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def CreateDocumentRequest(self, files, params):
        '''
        新建文档
        '''
        s = db.session()
        data = []
        uids = params['uid[]'].split(',')
        for i, file in enumerate(files):
            # 上传
            file_name = file.filename
            ext = self.file_extension(file_name)
            size = len(file.read())
            file_status = params['status']
            if not self.allowed_file(file_name):
                file_status = 2

            try:
                file.seek(0)
                fn = '/' + str(time.strftime('%Y/%m/%d'))
                if not os.path.exists(document_dir + fn):
                    os.makedirs(document_dir + fn)
                path = fn + '/' + str(uuid.uuid1()) + '.' + ext
                file.save(document_dir + path)

                item = Document(
                    document_id=uuid.uuid4(),
                    admin_id=params['admin_id'],
                    name=file_name,
                    status=file_status,
                    ext=ext,
                    path=path,
                    size=size,
                    folder_id=params['folder_id']
                )
                s.add(item)
                s.commit()
                data.append({
                    'name': file_name,
                    'size': size,
                    'status': file_status,
                    'src': path,
                    'uid': uids[i],
                    'res': 1
                })
            except Exception as e:
                print e
                s.rollback()
                data.append({
                    'uid': uids[i],
                    'res': 2
                })

        return data

    def GetDocumentRequest(self, document_id):
        '''
        查询文档
        '''
        s = db.session()
        try:
            document = s.query(Document).filter(Document.document_id == document_id).first()
            if not document:
                return str('文档不存在')

            return document.to_json()
        except Exception as e:
            print e
            return str(e.message)

    def RetrieveDocument(self, document_id, deleted):
        '''
        移动文档到回收站
        '''
        s = db.session()
        try:
            s.query(Document).filter(Document.document_id.in_(document_id)).update({Document.deleted: deleted}, synchronize_session=False)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def DelDocument(self, document_id):
        '''
        删除文档（包括服务器上文件）
        '''
        s = db.session()
        try:
            res = s.query(Document).filter(Document.document_id.in_(document_id))

            for i in res:
                s.delete(i)
                if os.path.exists(document_dir + i.path):
                    os.remove(document_dir + i.path)
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
