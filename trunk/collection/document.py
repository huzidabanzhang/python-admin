#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 上传控制层
@Author: Zpp
@Date: 2019-10-14 14:53:05
@LastEditors: Zpp
@LastEditTime: 2019-10-17 14:47:27
'''
from flask import request
from models.base import db
from models.system import Document
from conf.setting import document_dir
import uuid
import time


class DocumentModel():
    def QueryDocumentByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        文档列表
        '''
        s = db.session()
        try:
            Int = ['type', 'deleted']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Document.query.filter_by(*data).filter(
                Document.name.like("%" + params['name'] + "%") if params.has_key('name') else ''
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)

    def file_extension(self, filename):
        ary = filename.split('.')
        count = len(ary)
        return ary[count - 1] if count > 1 else ''

    def CreateDocumentRequest(self, file, params):
        '''
        新建文档
        '''
        s = db.session()
        try:
            # 上传
            file_name = file.filename
            ext = self.file_extension(file_name)
            size = len(file.read())

            fn = '/' + str(time.strftime('%Y/%m/%d'))
            if not os.path.exists(document_dir + fn):
                os.makedirs(document_dir + fn)
            path = fn + '/' + str(uuid.uuid1()) + '.' + ext
            file.save(document_dir + path)

            item = Document(
                document_id=uuid.uuid4,
                admin_id=params['admin_id'],
                name=file_name,
                type=params['type'],
                ext=ext,
                path=path,
                size=size
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

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

    def DelDocumentRequest(self, document_id):
        '''
        删除文档
        '''
        s = db.session()
        try:
            for key in document_id:
                document = s.query(Document).filter(Document.document_id == key).first()
                if not document:
                    continue
                document.deleted = 1
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)
