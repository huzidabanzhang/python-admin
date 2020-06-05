#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹API
@Author: Zpp
@Date: 2019-12-23 15:42:19
@LastEditors: Zpp
@LastEditTime: 2020-06-05 09:53:03
'''
from flask import Blueprint, request, session
from collection.v1.folder import FolderModel
from ..token_auth import auth, validate_current_access, get_auth_token
from libs.code import ResultDeal
from validate import validate_form
from validate.v1.folder import params

route_folder = Blueprint('Folder', __name__, url_prefix='/v1/Folder')
validate = validate_form(params)


@route_folder.route('/CreateFolder', methods=['POST'], endpoint='CreateFolder')
@auth.login_required
@validate_current_access
@validate.form('Create')
def CreateFolder():
    result = FolderModel().CreateFolderRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/DelFolder', methods=['POST'], endpoint='DelFolder')
@auth.login_required
@validate_current_access
@validate.form('Del')
def DelFolder():
    result = FolderModel().DelFolderRequest(request.form.get('folder_id'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/ModifyFolder', methods=['POST'], endpoint='ModifyFolder')
@auth.login_required
@validate_current_access
@validate.form('Modify')
def ModifyFolder():
    params = {'name': request.form.get('name')}
    if request.form.get('pid') != None:
        params['pid'] = request.form.get('pid')

    result = FolderModel().ModifyFolderRequest(request.form.get('folder_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/QueryFolderByParam', methods=['POST'], endpoint='QueryFolderByParam')
@auth.login_required
@validate_current_access
@validate.form('Query')
def QueryFolderByParam():
    result = FolderModel().QueryFolderByParamRequest(
        pid=request.form.get('pid'),
        admin_id=request.form.get('admin_id')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
