#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 文件夹API
@Author: Zpp
@Date: 2019-12-23 15:42:19
@LastEditors  : Please set LastEditors
@LastEditTime : 2020-02-14 14:51:54
'''
from flask import Blueprint, request, session
from collection.folder import FolderModel
from ..token_auth import auth, validate_current_access, get_auth_token
from libs.code import ResultDeal

route_folder = Blueprint('Folder', __name__, url_prefix='/v1/Folder')


@route_folder.route('/CreateFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateFolder():
    user = get_auth_token(session.get('admin'))
    params = {
        'pid': request.form.get('pid', '0'),
        'name': request.form.get('name'),
        'admin_id': user.get('admin_id')
    }

    result = FolderModel().CreateFolderRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/DelFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def DelFolder():
    result = FolderModel().DelFolderRequest(folder_id=request.form.get('folder_id'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_folder.route('/ModifyFolder', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyFolder():
    params = {
        'pid': request.form.get('pid', '0'),
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
    user = get_auth_token(session.get('admin'))
    result = FolderModel().QueryFolderByParamRequest(
        pid=request.form.get('pid', '0'),
        admin_id=user.get('admin_id')
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
