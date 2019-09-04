# -*- coding:UTF-8 -*-
# trunk/services/__init__.py
from conf.setting import server_info, mysql_info, token_info


def init_app(app):
    # 启动服务
    app.config.from_object(server_info)
    # session
    app.config['SECRET_KEY'] = token_info['SECRET_KEY']
