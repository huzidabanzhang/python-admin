from lib.service import server  # 提供服务
from conf.setting import server_info  # 导入启动参数

server.run(**server_info)  # 启动服务