#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 工资记录控制器
@Author: Zpp
@Date: 2020-04-10 13:30:34
@LastEditors: Zpp
@LastEditTime: 2020-04-22 15:53:50
'''
from flask import request
from models import db
from models.salary import Salary, SalaryUser, Attendance
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

class SalaryModel():
    def __init__(self):
        self.phone = re.compile('^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1|8|9]))\d{8}$')
        self.id_card = re.compile('^\d{6}(18|19|20)\d{2}(0\d|10|11|12)([0-2]\d|30|31)\d{3}[\dXx]$')

    def QuerySalaryByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        工资列表
        '''
        s = db.session()
        try:
            data = {}
            for i in ['payment_time']:
                if params.has_key(i):
                    data[i] = datetime.datetime.strptime(params[i], "%Y-%m")

            result = Salary.query.filter_by(**data).filter(
                Salary.company.like('%' + params['company'] + '%') if params.has_key('company') else text(''),
                Salary.name.like('%' + params['name'] + '%') if params.has_key('name') else text('')
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取工资列表失败%s' % e)
            return str('获取工资列表失败')

    def GetSalaryRequest(self, openid, page=1, page_size=20):
        '''
        获取个人工资列表
        '''
        s = db.session()
        try:
            res = SalaryUser.query.filter_by(**{
                'openid': openid
            }).first()

            if not res:
                return {'data': [], 'total': 0}

            data = {
                'id_card': res.id_card,
                'phone': res.phone
            }

            result = Salary.query.filter_by(**data).order_by('id').paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取个人工资失败%s' % e)
            return str('获取个人工资失败')

    def AddSalaryRequest(self, params):
        '''
        注册或者登录个人工资查询
        '''
        s = db.session()
        try:
            res = SalaryUser.query.filter_by(**{
                'id_card': params['id_card'],
                'phone': int(params['phone'])
            }).first()

            if res:
                return {
                    'openid': res.openid
                }

            openid = str(uuid.uuid4())

            s.add(SalaryUser(
                salary_user_id=uuid.uuid4(),
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

    def DelSalaryRequest(self, rid):
        '''
        删除工资记录
        '''
        s = db.session()
        try:
            result = s.query(Salary).filter(Salary.salary_id.in_(rid)).all()
            for i in result:
                s.delete(i)
            s.commit()
            return True
        except Exception as e:
            print e
            logging.info('-------删除工资记录失败%s' % e)
            return str('删除工资记录失败')

    def QueryAttendanceByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        获取考勤列表
        '''
        s = db.session()
        try:
            data = {}
            for i in ['attendance_time']:
                if params.has_key(i):
                    data[i] = datetime.datetime.strptime(params[i], "%Y-%m")

            result = Attendance.query.filter_by(**data).filter(
                Attendance.name.like('%' + params['name'] + '%') if params.has_key('name') else text('')
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取考勤列表失败%s' % e)
            return str('获取考勤列表失败')

    def GetAttendanceRequest(self, params, page=1, page_size=20):
        '''
        获取个人考勤列表
        '''
        s = db.session()
        try:
            data = {
                'name': params['name'],
                'user_id': params['user_id']
            }

            result = Attendance.query.filter_by(**data).order_by('id').paginate(page, page_size, error_out=False)

            return {'data': [value.to_json() for value in result.items], 'total': result.total}
        except Exception as e:
            print e
            logging.info('-------获取个人考勤列表失败%s' % e)
            return str('获取个人考勤列表失败')

    def DelAttendanceRequest(self, rid):
        '''
        删除考勤记录
        '''
        s = db.session()
        try:
            result = s.query(Attendance).filter(Attendance.attendance_id.in_(rid)).all()
            for i in result:
                s.delete(i)
            s.commit()
            return True
        except Exception as e:
            print e
            logging.info('-------删除考勤记录失败%s' % e)
            return str('删除考勤记录失败')

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

                d = {'value': [], 'row': rows, 'sheet': name}
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
                            d['value'].append({
                                'name': j,
                                'value': self.excel_fileds(i[index], sheet.cell(row, index).ctype)
                            })
                if is_error == False:           
                    params.append(d)

        return {
            'data': params,
            'error': error
        }

    def ImportSalaryRequest(self, file, payment_time):
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
            
            all_list = Salary.query.filter_by(**{
                'payment_time': datetime.datetime.strptime(payment_time, "%Y-%m")
            }).all()

            ic_list = [res.id_card for res in all_list]

            case = []
            for i in data['data']:
                if not i[u'身份证'] in ic_list:
                    try:
                        case.append(Salary(
                            salary_id=uuid.uuid4(),
                            company=i[u'公司'],
                            name=i[u'姓名'],
                            id_card=i[u'身份证'],
                            phone=int(i[u'电话']),
                            salary=json.dumps(i['value']),
                            payment_time=datetime.datetime.strptime(payment_time, "%Y-%m")
                        ))
                    except Exception as e:
                        print e
                        logging.info('-------导入工资列表失败%s' % e)
                        error.append(u'%s表第%s行添加失败' % (i['sheet'], i['row']))
                        continue
            s.add_all(case)
            s.commit()
            return error
        except Exception as e:
            print e
            logging.info('-------导入工资列表失败%s' % e)
            return str('导入工资列表失败')

    def excel_fileds(self, data, ctype):
        '''
        处理excel字段
        '''
        try:
            if ctype == 2 and data - int(data) == 0:
                v = int(data)
            elif ctype == 3:
                if data < 64:
                    t = (1900, 1, 1, 0, 0, 0)
                else:
                    t = xlrd.xldate_as_tuple(data, 0)
                v = datetime.datetime(*t)
                v = v.strftime('%Y-%m-%d')
            elif ctype == 4:
                v = True if data == 1 else False
            else:
                v = str(data)

            return v
        except:
            return data

    def ImportAttendanceRequest(self, file, attendance_time):
        '''
        导入考勤记录
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

            params = []
            for name in wb.sheet_names():
                try:
                    sheet = wb.sheet_by_name(name)
                    item = sheet.row_values(0)
                    item = [i.replace(" ", "") if type(i) == unicode else self.excel_fileds(i, sheet.cell(0, index).ctype) for index, i in enumerate(item)]

                    fileds = {
                        'name': item.index(u'姓名'),
                        'company': item.index(u'公司名称')
                    }

                    # 冠捷逻辑
                    if u'时数' in item:
                        d = {}

                        for row in range(1, sheet.nrows):
                            i = sheet.row_values(row)
                            rows = row + 1

                            if i[fileds['name']] == '':
                                continue

                            name = i[fileds['name']].replace(" ", "")
                            if not d.has_key(name):
                                d[name] = {
                                    'company': i[fileds['company']],
                                    'user_id': i[item.index(u'人员编号')],
                                    'content': [],
                                    'attance': {}
                                }

                            current = self.excel_fileds(i[item.index(u'当前日期')], sheet.cell(row, item.index(u'当前日期')).ctype)
                            duration = self.excel_fileds(i[item.index(u'时数')], sheet.cell(row, item.index(u'时数')).ctype)
                            types = self.excel_fileds(i[item.index(u'类型')], sheet.cell(row, item.index(u'类型')).ctype)

                            if d[name]['attance'].has_key(current):
                                d[name]['attance'][current] += u'<br>%s：%s小时' % (types, duration)
                            else:
                                d[name]['attance'][current] = u'%s：%s小时' % (types, duration)

                        for j in d:
                            d_data = d[j]
                            d_data['name'] = j

                            attance = []
                            for x in d[j]['attance']:
                                attance.append({
                                    'name': x,
                                    'value': d[j]['attance'][x]
                                })

                            d_data['attance'] = attance
                            params.append(d_data)

                    # 友达的逻辑
                    if u'总工时' in item:
                        total = {
                            u'部门': item.index(u'部门'),
                            u'转正日期': item.index(u'转正日期'),
                            u'总工时': item.index(u'总工时')
                        }

                        for row in range(1, sheet.nrows):
                            # 读取所有内容
                            i = sheet.row_values(row)
                            rows = row + 1
                            data = {
                                'content': [],
                                'attance': []
                            }

                            if i[fileds['name']] == '':
                                continue

                            for j in fileds:
                                data[j] = self.excel_fileds(i[fileds[j]], sheet.cell(row, fileds[j]).ctype)
                            data['user_id'] = self.excel_fileds(i[item.index(u'工号')], sheet.cell(row, item.index(u'工号')).ctype)
                            for j in total:
                                data['content'].append({
                                    'name': j,
                                    'value': self.excel_fileds(i[total[j]], sheet.cell(row, total[j]).ctype)
                                })
                            for j in range(total[u'总工时'] + 1, len(i)):
                                data['attance'].append({
                                    'name': item[j],
                                    'value': u'%s 小时' % i[j]
                                })

                            params.append(data)
                except Exception as e:
                    print e
                    continue

            case = []
            for i in params:
                try:
                    case.append(Attendance(
                        attendance_id=uuid.uuid4(),
                        company=i['company'],
                        name=i['name'],
                        user_id=i['user_id'],
                        content=json.dumps(i['content']),
                        attance=json.dumps(i['attance']),
                        attendance_time=datetime.datetime.strptime(attendance_time, "%Y-%m")
                    ))
                except Exception as e:
                    print e
                    logging.info('-------导入考勤记录失败%s' % e)
                    continue
            s.add_all(case)
            s.commit()
            return True
        except Exception as e:
            print e
            logging.info('-------导入考勤记录失败%s' % e)
            return str('导入考勤记录失败')
