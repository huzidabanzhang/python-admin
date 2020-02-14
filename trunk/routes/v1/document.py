#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 附件API
@Author: Zpp
@Date: 2019-10-14 15:56:20
@LastEditors  : Please set LastEditors
@LastEditTime : 2020-02-14 14:59:26
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
        'type': int(request.form.get('type')),
        'uid': request.form.getlist('uid'),
        'folder_id': request.form.get('folder_id', None)
    }

    files = request.files.getlist('document')
    if not files:
        return ResultDeal(msg=u'请选择上传文件', code=-1)

    result = DocumentModel().CreateDocumentRequest(files, params)
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


@route_document.route('/RetrieveDocument', methods=['POST'])
@auth.login_required
@validate_current_access
def RetrieveDocument():
    result = DocumentModel().RetrieveDocument(document_id=request.form.getlist('document_id'))
    return ResultDeal(data=result)


@route_document.route('/DelDocument', methods=['POST'])
@auth.login_required
@validate_current_access
def DelDocument():
    result = DocumentModel().DelDocument(document_id=request.form.getlist('document_id'))
    return ResultDeal(data=result)


@route_document.route('/QueryDocumentByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryDocumentByParam():
    params = {}
    Ary = ['status', 'deleted', 'folder_id']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = DocumentModel().QueryDocumentByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
