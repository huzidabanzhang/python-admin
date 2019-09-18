#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志初始化
@Author: Zpp
@Date: 2019-09-12 16:38:25
@LastEditors: Zpp
@LastEditTime: 2019-09-18 15:00:42
'''
import logging
from logging.handlers import TimedRotatingFileHandler
from conf.setting import log_info


def init_app():
    formatter = logging.Formatter('%(asctime)s - %(module)s %(filename)s %(funcName)s:%(lineno)s - %(name)s -%(message)s')

    logging.root.setLevel(logging.INFO)
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    console.addFilter(logging.Filter())
    logging.root.addHandler(console)

    file_handler_info = TimedRotatingFileHandler(filename=log_info['LOG_PATH_INFO'], backupCount=log_info['LOG_FILE_BACKUP_COUNT'], when='D', interval=1, encoding='utf-8')
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.addFilter(logging.Filter())
    logging.root.addHandler(file_handler_info)

    return True
