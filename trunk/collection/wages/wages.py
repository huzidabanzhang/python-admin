#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录控制器
@Author: Zpp
@Date: 2020-04-10 13:30:34
@LastEditors: Zpp
@LastEditTime: 2020-04-14 13:28:59
'''
from flask import request
from models import db
from models.wages import Wages, WagesUser
from sqlalchemy import text
from conf.setting import excel_dir
from libs.aliyun import AliyunModel
import logging
import xlrd
import uuid
import time
import os
import datetime
import json
import re

class WagesModel():
    def __init__(self):
        self.phone = re.compile('^1[35678]\d{9}$')
        self.id_card = re.compile('^\d{6}(18|19|20)\d{2}(0\d|10|11|12)([0-2]\d|30|31)\d{3}[\dXx]$')

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
            res = WagesUser.query.filter_by(**{
                'openid': openid
            }).first()

            if not res:
                return str('请先注册')
            print res
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
        注册或者登录个人工资查询
        '''
        s = db.session()
        try:
            res = WagesUser.query.filter_by(**{
                'id_card': params['id_card'],
                'phone': int(params['phone'])
            }).first()

            if res:
                return {
                    'openid': res.openid
                }

            openid = str(uuid.uuid4())

            s.add(WagesUser(
                wages_user_id=uuid.uuid4(),
                id_card=params['id_card'],
                phone=int(params['phone']),
                openid=openid
            ))
            s.commit()
            return {
                'openid': openid
            }
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

    def deal_data(self, wb):
        '''
        处理excel内容
        '''
        params = []
        error = []
        fileds = [u'公司', u'姓名', u'身份证', u'电话']

        for name in wb.sheet_names():
            sheet = wb.sheet_by_name(name)
            item = []
            for row in range(sheet.nrows):
                # 读取所有内容
                i = sheet.row_values(row)
                rows = row + 1
                if i[0] == u'公司':
                    for x in i:
                        item.append(x.replace(" ", ""))

                    if not u'公司' in item or not u'姓名' in item or not u'身份证' in item or not u'电话' in item:
                        error.append(u'%s请输入必须公司，姓名，身份证和电话的表头' % name)
                        break
                    else:
                        continue

                d = {'value': {}, 'row': rows, 'sheet': name}
                is_error = False
                for index, j in enumerate(item):
                    if j:
                        if j in fileds:
                            d[j] = i[index] if type(i[index]) != float else int(i[index])

                            if j == u'身份证' and not self.id_card.match(d[j]):
                                is_error = True
                                error.append(u'%s表第%s行，身份证格式不正确' % (name, rows))
                                break
                            if j == u'电话' and not self.phone.match(str(d[j])):
                                is_error = True
                                error.append(u'%s表第%s行，电话格式不正确' % (name, rows))
                                break
                            if i[index] == '' and i[index] == None:
                                is_error = True
                                error.append(u'%s表第%s行，%s不能为空' % (name, rows, j))
                                break
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
                if is_error == False:           
                    params.append(d)

        return {
            'data': params,
            'error': error
        }

    def ImportWagesRequest(self, file, payment_time):
        '''
        导入工资记录
        '''
        s = db.session()
        try:
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

            wb = xlrd.open_workbook(excel_dir + path)
            data = self.deal_data(wb)
            error = data['error']
            
            all_list = Wages.query.filter_by(**{
                'payment_time': datetime.datetime.strptime(payment_time, "%Y-%m")
            }).all()

            ic_list = [res.id_card for res in all_list]

            case = []
            for i in data['data']:
                if not i[u'身份证'] in ic_list:
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
                        error.append(u'%s表第%s行添加失败' % (i['sheet'], i['row']))
                        continue
            s.add_all(case)
            s.commit()
            return error
        except Exception as e:
            print e
            logging.info('-------获取工资列表失败%s' % e)
            return str('获取工资列表失败')
