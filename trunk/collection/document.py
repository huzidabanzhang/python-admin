#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 上传控制层
@Author: Zpp
@Date: 2019-10-14 14:53:05
@LastEditors: Zpp
@LastEditTime: 2019-10-14 15:11:53
'''
from flask import request
from models.base import db
from models.system import Document
from libs.error_code import RecordLog
import uuid


class DocumentModel():
    def QueryDocumentByParamRequest(self, params, page=1, page_size=20, order_by='-id'):
        '''
        文档列表
        '''
        s = db.session()
        try:
            Int = ['type']
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
            return RecordLog(request.url, e)
        finally:
            s.close()

    def CreateDocumentRequest(self, fiel, params):
        '''
        新建文档
        '''
        s = db.session()
        try:
            #上传

            item = Document(
                document_id=uuid.uuid4,
                user_id=params['user_id'],
                name=params['name'],
                type=params['type']
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return RecordLog(request.url, e)
        finally:
            s.close()

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
            return RecordLog(request.url, e)
        finally:
            s.close()

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
                document.delete()
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return RecordLog(request.url, e)
        finally:
            s.close()
