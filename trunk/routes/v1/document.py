#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文档API
@Author: Zpp
@Date: 2019-10-14 15:56:20
@LastEditors: Zpp
@LastEditTime: 2019-11-08 14:37:45
'''
from flask import Blueprint, request, make_response, abort, send_from_directory
from collection.document import DocumentModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal
from conf.setting import document_dir
from libs.utils import readFile
import os
import base64
import mimetypes

route_document = Blueprint('Document', __name__, url_prefix='/v1/Document')


@route_document.route('/CreateDocument', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateDocument():
    params = {
        'admin_id': request.form.get('admin_id'),
        'type': int(request.form.get('type'))
    }

    file = request.files['document']
    if not file:
        return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = DocumentModel().CreateDocumentRequest(file, params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_document.route('/GetDocument/<path:filename>', methods=['GET'])
def GetDocument(filename):
    path = document_dir + '/' + filename
    if os.path.exists(path):
        return send_from_directory(document_dir, filename)
    else:
        abort(404)


@route_document.route('/DownDocument/<path:filename>/<name>', methods=['GET'])
@auth.login_required
@validate_current_access
def DownDocument(filename, name):
    path = document_dir + '/' + filename
    if os.path.exists(path):
        res = make_response(readFile(path, 'rb'))
        res.headers['Content-Type'] = 'application/octet-stream'
        res.headers['Content-Disposition'] = 'attachment; filename=' + name
        return res
    else:
        abort(404)


@route_document.route('/DelDocument', methods=['POST'])
@auth.login_required
@validate_current_access
def LockDocument():
    result = DocumentModel().DelDocumentRequest(document_id=request.form.getlist('document_id'))
    return ResultDeal(data=result)


@route_document.route('/QueryDocumentByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryDocumentByParam():
    params = request.form
    Int = ['type', 'deleted']
    for i in params:
        if i in Int:
            params[i] = int(params[i])

    result = DocumentModel().QueryDocumentByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
