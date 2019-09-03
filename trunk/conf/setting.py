# token 基本参数
token_info = {
    'expiration': 30 * 24 * 3600,
    'user_name': 'zpp',
    'password': 'python',
    'SECRET_KEY': 'k#6@1%8)a'
}

#mysql 配置信息 字典类型
mysql_info = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'intersky',
    'db': '***',
    'charset': 'utf8',
    'autocommit': True
}

#启动服务参数 字典类型
server_info = {
    "host": '0.0.0.0',
    "port": 5000,  # 启动服务的端口号
    'debug': True  # 是否是调试模式
}
