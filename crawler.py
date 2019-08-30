# -*- coding:utf-8 -*-
'''
Created Date: 2019-4-4

'''
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from dateutil.parser import parse
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import text
from flask import Flask, jsonify, request
import codecs
import pymysql
import time
import re
import json


class Fit():
    def __init__(self):
        self.url = 'https://www.hiyd.com/dongzuo/?equipment=3'  # 暂定为徒手训练
        self.base_url = 'https://www.hiyd.com'
        self.file_url = 'e:\motion.json'
        self.titleClass = '.menu-item-bd .sort-item'
        self.position = '.training-part'
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self.TYPE = {
            u'初级': 6,
            u'中级': 9,
            u'高级': 11
        }
        self.POSITION = []

        # print('------------------chrome初始化开始-----------------')
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
        # self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='D:\chromedriver.exe')

    def getUrlContent(self):
        print('------------------抓取开始  %s-----------------' % self.time)
        try:
            res = requests.get(self.url)
            soup = BeautifulSoup(res.text, 'html.parser')

            self.getPosition(soup=soup)
            # 删除不限部位
            del self.POSITION[0]

            for item in self.POSITION:
                print(item['name'])
                item['motion'] = self.getMotionDes(item['href'])
                print(item['motion'])

            # 抓取完后释放
            # self.browser.quit()
            # 暂时写入json文件中
            fp = open(self.file_url, 'w')
            json_data = json.dumps(self.POSITION, sort_keys=True, indent=4)
            fp.write(json_data)
            fp.close()

            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print('------------------抓取完成  %s-----------------' % now_time)
            print('------------------耗时  %s-----------------' % (parse(now_time) - parse(self.time)).seconds)
            return True
        except:
            return False

    def getPosition(self, soup):
        for position in soup.select('%s %s' % (self.position, self.titleClass)):
            self.POSITION.append({
                'name': position.get_text().strip(),
                'href': position.get('href'),
                'motion': []
            })

    def getMotionDes(self, url):
        data = []
        sexs = [1, 2]
        for type in self.TYPE:
            hasContent = True
            page_no = 1
            while hasContent == True:
                try:
                    res = requests.get('%s&difficulty=%d&page=%d' % (url, self.TYPE[type], page_no))
                    soup = BeautifulSoup(res.text, 'html.parser')
                    if len(soup.select('.hvr-glow')) < 1:
                        hasContent = False
                    else:
                        page_no += 1
                        for item in soup.select('.hvr-glow'):
                            tag = []
                            for tags in item.select('.tag span'):
                                tag.append(tags.get_text().strip())
                            for sex in sexs:
                                data.append({
                                    'name': item.select('.title')[0].get_text().strip(),
                                    'des': ' '.join(tag),
                                    'src': item.select('.avatar-pic img')[0].get('src'),
                                    'data': self.getMotionVideo(item.select('a[href]')[0].get('href'), sex),
                                    'type': self.TYPE[type],
                                    'sex': sex
                                })
                except:
                    hasContent = False
        return data

    def getMotionVideo(self, url, sex):
        # 异步js加载后抓取（暂时不用了）
        # self.browser.get('%s%s' % (self.base_url, url))
        # self.browser.add_cookie({
        #     'domain': '.hiyd.com',
        #     'name': 'coach_gender',
        #     'value': '2',
        #     'path': '/',
        #     'expires': None
        # })
        # self.browser.get('%s%s' % (self.base_url, url))
        # # 等待页面加载video后
        # is_hasContent = True
        # count = 1
        # while is_hasContent == True and count < 5:
        #     src = self.browser.find_element_by_tag_name("video").get_attribute('src')
        #     if not src:
        #         count += 1
        #         time.sleep(0.5)
        #     else:
        #         is_hasContent = False
        # print(src)
        # return src

        # 正则提取script中json数据
        cookie = RequestsCookieJar()
        cookie.set('coach_gender', str(sex), domain='.hiyd.com')
        res = requests.get('%s%s' % (self.base_url, url), cookies=cookie)
        soup = BeautifulSoup(res.text, 'html.parser')
        script = soup.find_all('script')
        # 获取最后一个script钟的json
        jsondata = json.loads(re.search(r'init\(([\s\S]*?)\)', str(script[len(script) - 1])).group(1))

        if not jsondata['muscle_pic']:
            muscle = [
                jsondata['muscle_front_img'],
                jsondata['muscle_back_img']
            ]
        else:
            muscle = []

        data = {
            'description': jsondata['description'],
            'gif': jsondata['video_url'],
            'image': muscle,
            'step': jsondata['exe_explain_pic']
        }
        print(data)
        return json.dumps(data)


class Keep():
    def __init__(self):
        self.url = 'http://api.gotokeep.com/training/v3/course/selectors'
        self.file_url = 'e:\motion.json'
        self.params = {"size": 50, "sortType": "default",
                       "selectors":
                           {
                               "5b602010d734a23693108a8d": ["54826e417fb786000069ad86", "54826e417fb786000069ad85",
                                                            "54826e417fb786000069ad81"],
                               "5b602010d734a23693108a8c": ["54826e417fb786000069ad80", "54826e417fb786000069ad59"],
                               "5b601b4da29e3438df219192": ["1", "2"]
                           },
                       "subCategory": "normal", "category": "training"}
        self.headers = {'Content-Type': 'application/json'}

    def getData(self):
        Course = []
        isLast = False
        params = self.params
        lastId = ''

        while isLast == False:
            try:
                if lastId != '':
                    params['lastId'] = lastId
                result = self.urlPost(self.url, params)

                if result['errorCode'] == 0:
                    for item in result['data']['datas']:
                        Course.append(item)
                    if result['data']['lastId']:
                        lastId = result['data']['lastId']
                    else:
                        isLast = True
                else:
                    isLast = True
            except:
                isLast = True

        for item in Course:
            url = 'http://api.gotokeep.com/course/v3/plans/%s?trainer_gender=F' % item['id']
            result = self.urlGet(url)
            item['actions'] = result['data']

        fp = open(self.file_url, 'w')
        json_data = json.dumps(Course, sort_keys=True, indent=4)
        fp.write(json_data)
        fp.close()

        return True

    def urlGet(self, url):
        result = requests.get(url)
        return json.loads(result.text)

    def urlPost(self, url, params):
        result = requests.post(url, data=json.dumps(params), headers=self.headers)
        return json.loads(result.text)


if __name__ == '__main__':
    pass