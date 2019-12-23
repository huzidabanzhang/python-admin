#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹API
@Author: Zpp
@Date: 2019-12-23 15:42:19
@LastEditors  : Zpp
@LastEditTime : 2019-12-23 15:45:49
'''
from flask import Blueprint, request
from collection.folder import FolderModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_folder = Blueprint('Folder', __name__, url_prefix='/v1/Folder')


@route_folder.route('/CreateFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateFolder():
    params = {
        'parent_id': request.form.get('parent_id', '0'),
        'name': request.form.get('name')
    }

    result = FolderModel().CreateFolderRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/DelFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def DelFolder():
    result = FolderModel().DelFolderRequest(
        folder_id=request.form.get('folder_id'),
        isFolder=True if request.form.get('isFolder') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/GetFolder/<folder_id>', methods=['GET'])
@auth.login_required
@validate_current_access
def GetFolder(folder_id):
    result = FolderModel().GetFolderRequest(folder_id=folder_id)
    return ResultDeal(data=result)


@route_folder.route('/ModifyFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyFolder():
    params = {
        'parent_id': request.form.get('parent_id', '0'),
        'name': request.form.get('name')
    }

    result = FolderModel().ModifyFolderRequest(folder_id=request.form.get('folder_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/QueryFolderByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryFolderByParam():
    result = FolderModel().QueryFolderByParamRequest()

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
