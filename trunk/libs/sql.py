#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2020-02-19 19:45:33
@LastEditTime: 2020-02-20 19:17:46
@LastEditors: Please set LastEditors
'''

from conf.setting import Config, sql_dir
import os
import time


class SqlModel():
    def read_sql(self):
        config = Config()
        if not os.path.exists(sql_dir):
            os.mkdir(sql_dir)

        os.chdir(sql_dir)
        filename = 'TABLE%s.sql' % int(time.time() * 1000)
        
        # mysqldump 命令
        sqlfromat = "%s -h%s -u%s -p%s -P%s %s >%s"
        # 生成相应的sql语句
        sql = (sqlfromat % ('mysqldump ',
                            config.host,
                            config.admin,
                            config.password,
                            config.port,
                            config.db,
                            filename))
        os.system(sql)

    def white_sql(self):
        config = Config()
        file = os.path.join(sql_dir, 'TABLE1582197200631.sql')
        print file
        
        sqlfromat = "%s -h%s -u%s -p%s -P%s %s <%s"
        sql = (sqlfromat % ('mysql ',
                            config.host,
                            config.admin,
                            config.password,
                            config.port,
                            config.db,
                            file))
        print sql
        os.system(sql)
