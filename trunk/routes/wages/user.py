#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资查询API
@Author: Zpp
@Date: 2020-04-13 13:07:43
@LastEditors: Zpp
@LastEditTime: 2020-04-13 14:05:21
'''
from flask import Blueprint, request, session
from collection.wages.wages import WagesModel
from libs.code import ResultDeal
from conf.aliyun import wx_info
import urllib
import json
import datetime

route_wages_user = Blueprint('WagesUser', __name__, url_prefix='/wages/User')


# 获取openid
@route_wages_user.route('/GetOpenId', methods=['POST'])
def GetOpenId():
    code = request.form.get('code')

    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (wx_info['appid'], wx_info['secret'], code)

    html = urllib.urlopen(url)
    html = json.loads(html.read())

    if html['openid']:
        return ResultDeal(data=html['openid'])
    else:
        return ResultDeal(code=-1, msg=html['errmsg'])


@route_wages_user.route('/GetCode', methods=['POST'])
def GetCode():
    result = WagesModel().GetCodeRequest(request.form.get('phone'))

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_wages_user.route('/AddWages', methods=['POST'])
def AddWages():
    if not request.form.get('code'):
        return ResultDeal(msg=u'请输入验证码', code=-1)

    Code = session.get('Code')

    if not Code:
        return ResultDeal(msg=u'请获取验证码', code=-1)

    if (datetime.datetime.now() - Code['time']).seconds > 5 * 60:
        return ResultDeal(msg=u'验证码已过期', code=-1)

    if Code['code'] != request.form.get('code'):
        return ResultDeal(msg=u'验证码不正确', code=-1)

    result = WagesModel().AddWagesRequest(request.form)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_wages_user.route('/GetWages', methods=['POST'])
def GetWages():
    if not request.form.get('openid'):
        return ResultDeal(msg=u'请先注册', code=-1)

    result = WagesModel().GetWagesRequest(
        openid=request.form.get('openid'),
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size'))
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
