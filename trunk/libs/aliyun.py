#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 阿里云短信
@Author: Zpp
@Date: 2020-04-13 10:30:25
@LastEditors: Zpp
@LastEditTime: 2020-04-15 09:43:58
'''

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from conf.aliyun import ali_info
from flask import session
import json
import string
import random
import datetime


class AliyunModel():
    def get_code(self):
        return "".join(random.sample(string.digits, 4))

    def SmsSend(self, phone):
        code = self.get_code()
        client = AcsClient(ali_info['AccessKey'], ali_info['Secret'], 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', ali_info['SignName'])
        request.add_query_param('TemplateCode', ali_info['TemplateCode'])
        request.add_query_param('TemplateParam', json.dumps({
            'code': code
        }))

        response = json.loads(client.do_action(request))

        if response['Code'] == 'OK':
            session['Code'] = {
                'code': code,
                'time': datetime.datetime.now()
            }
            return True
        else:
            return str(response['Message'])

