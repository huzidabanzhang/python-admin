#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 附件API
@Author: Zpp
@Date: 2019-10-14 15:56:20
@LastEditors: Zpp
@LastEditTime: 2020-05-28 15:02:54
'''
from flask import Blueprint, request, make_response, abort, send_from_directory, session
from collection.v1.document import DocumentModel
from ..token_auth import auth, validate_current_access, get_auth_token
from libs.code import ResultDeal
from conf.setting import document_dir
from libs.utils import readFile
from validate import validate_form
from validate.v1.document import params
import os
import base64
import mimetypes

route_document = Blueprint('Document', __name__, url_prefix='/v1/Document')
validate = validate_form(params)


@route_document.route('/CreateDocument', methods=['POST'], endpoint='CreateDocument')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateDocument():
    result = DocumentModel().CreateDocumentRequest(
        request.files.getlist('document'),
        request.form
    )
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


@route_document.route('/RetrieveDocument', methods=['POST'], endpoint='RetrieveDocument')
@auth.login_required
@validate_current_access
@validate.form('Retrieve')
def RetrieveDocument():
    result = DocumentModel().RetrieveDocument(
        request.form.getlist('document_id[]'),
        request.form.get('deleted')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_document.route('/DelDocument', methods=['POST'], endpoint='DelDocument')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelDocument():
    result = DocumentModel().DelDocument(request.form.getlist('document_id[]'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_document.route('/QueryDocumentByParam', methods=['POST'], endpoint='QueryDocumentByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryDocumentByParam():
    params = {}
    Ary = ['status', 'deleted', 'folder_id']
    for i in Ary:
        if request.form.get(i) != None:
            params[i] = request.form.get(i)

    result = DocumentModel().QueryDocumentByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
