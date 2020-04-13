#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录控制器
@Author: Zpp
@Date: 2020-04-10 13:30:34
@LastEditors: Zpp
@LastEditTime: 2020-04-13 13:28:23
'''
from flask import request
from models import db
from models.wages import Wages, WagesUser
from sqlalchemy import text
from conf.setting import excel_dir
from libs.aliyun import AliyunModel
import logging
import xlwings as xw
import uuid
import time
import os
import datetime
import json


class WagesModel():
    def QueryWagesByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        工资列表
        '''
        s = db.session()
        try:
            data = {}
            for i in ['payment_time']:
                if params.has_key(i):
                    data[i] = datetime.datetime.strptime(params[i], "%Y-%m")

            result = Wages.query.filter_by(**data).filter(
                Wages.company.like('%' + params['company'] + '%') if params.has_key('company') else text(''),
                Wages.name.like('%' + params['name'] + '%') if params.has_key('name') else text('')
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取工资列表失败%s' % e)
            return str('获取工资列表失败')

    def GetWagesRequest(self, openid, page=1, page_size=20):
        '''
        获取个人工资列表
        '''
        s = db.session()
        try:
            res = WagesUser.query.filter_by({
                'openid': openid
            }).first()

            if not res:
                return str('请先注册')

            data = {
                'id_card': res.id_card,
                'phone': res.phone
            }

            result = Wages.query.filter_by(**data).order_by('id').paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取个人工资失败%s' % e)
            return str('获取个人工资失败')

    def AddWagesRequest(self, params):
        '''
        注册个人工资查询
        '''
        s = db.session()
        try:
            WagesUser(
                wages_user_id=uuid.uuid4(),
                id_card=params['id_card'],
                phone=int(params['phone']),
                openid=params['openid']
            )

            s.add(WagesUser)
            s.commit()
            return True
        except Exception as e:
            print e
            logging.info('-------注册个人工资查询失败%s' % e)
            return str('注册个人工资查询失败')

    def GetCodeRequest(self, phone):
        '''
        获取阿里云短信
        '''
        if not phone:
            return str('请输入电话')

        res = AliyunModel().SmsSend(phone)

        return res
        

    @staticmethod
    def allowed_file(file):
        ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

        return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def ImportWagesRequest(self, file, payment_time):
        '''
        导入工资记录
        '''
        s = db.session()
        filename = file.filename

        ary = filename.split('.')
        count = len(ary)
        ext = ary[count - 1] if count > 1 else ''
        if not self.allowed_file(filename):
            return str('请上传Excel文件')

        file.seek(0)
        fn = '/' + str(time.strftime('%Y/%m/%d'))
        if not os.path.exists(excel_dir + fn):
            os.makedirs(excel_dir + fn)
        path = fn + '/' + str(uuid.uuid1()) + '.' + ext
        file.save(excel_dir + path)

        import pythoncom
        pythoncom.CoInitialize()

        xw_app = xw.App(visible=False, add_book=False)
        wb = xw_app.books.open(excel_dir + path)
        try:
            params = []

            for sheet in wb.sheets:
                # 读取所有内容
                data = sheet.range('A1').expand().value

                fileds = [u'公司', u'姓名', u'身份证', u'电话']
                for i in data:
                    if i[0] == u'公司':
                        item = i
                    else:
                        d = {
                            'value': {}
                        }
                        for index, j in enumerate(item):
                            if j:
                                if j.replace(" ", "") in fileds:
                                    d[j.replace(" ", "")] = i[index] if type(i[index]) != float else int(i[index])
                                else:
                                    v = i[index]
                                    if type(i[index]).__name__ == 'datetime':
                                        v = i[index].strftime('%Y-%m-%d')
                                    elif i[index] == None:
                                        v = ''
                                    elif type(i[index]) == float:
                                        if i[index] - int(i[index]) == 0:
                                            v = int(i[index])
                                    else:
                                        v = str(i[index])
                                    d['value'][j] = v
                        params.append(d)

            case = []
            for i in params:
                try:
                    case.append(Wages(
                        wages_id=uuid.uuid4(),
                        company=i[u'公司'],
                        name=i[u'姓名'],
                        id_card=i[u'身份证'],
                        phone=int(i[u'电话']),
                        wages=json.dumps(i['value']),
                        payment_time=datetime.datetime.strptime(payment_time, "%Y-%m")
                    ))
                except Exception as e:
                    print e
                    logging.info('-------新增工资记录失败%s' % e)
                    continue
            s.add_all(case)
            s.commit()
            return True
        except Exception as e:
            print e
            logging.info('-------获取工资列表失败%s' % e)
            return str('获取工资列表失败')
        finally:
            wb.close()
            xw_app.quit()
            xw_app.kill()
