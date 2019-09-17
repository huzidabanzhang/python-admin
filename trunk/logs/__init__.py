#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 日志初始化
@Author: Zpp
@Date: 2019-09-12 16:38:25
@LastEditors: Zpp
@LastEditTime: 2019-09-17 09:34:28
'''
import logging
from logging.handlers import TimedRotatingFileHandler
from conf.setting import log_info


def init_app(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(process)d %(thread)d '
        '%(pathname)s %(lineno)s %(message)s')
    info_filter = logging.Filter()

    # FileHandler Info
    file_handler_info = TimedRotatingFileHandler(filename=log_info['LOG_PATH_INFO'], backupCount=log_info['LOG_FILE_BACKUP_COUNT'], when='D', interval=1, encoding='utf-8')
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.addFilter(info_filter)
    app.logger.addHandler(file_handler_info)

    # FileHandler Error
    file_handler_error = TimedRotatingFileHandler(filename=log_info['LOG_PATH_ERROR'], backupCount=log_info['LOG_FILE_BACKUP_COUNT'], when='D', interval=1, encoding='utf-8')
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)
    file_handler_info.addFilter(info_filter)
    app.logger.addHandler(file_handler_error)

    return app
