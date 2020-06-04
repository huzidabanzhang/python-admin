#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 基本配置信息
@Author: Zpp
@Date: 2019-09-02 15:53:39
@LastEditTime: 2020-06-04 14:53:13
@LastEditors: Zpp
'''
import hashlib
import os
from libs.utils import isWindows

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')

base_info = {
    'lock_times': 5,  # 开始锁定的次数
    'lock_every_time': 5  # 超过锁定次数每次加的时间
}

token_info = {
    'expiration': 30 * 24 * 3600,
    'SECRET_KEY': 'k#6@1%8)a'
}

# 启动服务参数 字典类型
server_info = {
    "host": '0.0.0.0',
    "port": 92,  # 启动服务的端口号
}

# 文档路径
document_dir = os.path.join(basedir, 'document')

# excel存放路径
excel_dir = os.path.join(basedir, 'excel')

# GeoLite2路径
GeoLite2_dir = os.path.join(basedir, 'tools/GeoLite2-City.mmdb')

# sql下载临时路径
sql_dir = os.path.join(basedir, 'sql')

# 日志
log_info = {
    'LOG_FILE_BACKUP_COUNT': 0,
    'LOG_PATH_INFO': os.path.join(os.path.join(basedir, 'logs'), 'info.log')
}

# session参数
session_info = {
    'SESSION_TYPE': 'filesystem',
    'SESSION_FILE_DIR': os.path.join(basedir, 'sessions'),
    'SESSION_FILE_THRESHOLD': 500,
    'SESSION_FILE_MODE': 384,
    'SESSION_PERMANENT': True
}

# cache参数
cache_info = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': os.path.join(basedir, 'caches'),
    'CACHE_THRESHOLD': 500
}

# 初始化菜单和下属的接口
init_menu = [
    {
        "title": "系统",
        "path": "/system",
        "icon": "cog",
        "mark": "system",
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'name': 'System',
        'cache': True,
        "children": [
            {
                "title": "菜单管理",
                "path": "/system/menu",
                "icon": "th-list",
                "mark": "system_menu",
                'name': 'MenuPage',
                'component': 'menu',
                'componentPath': 'sys/menu/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Menu/CreateMenu",
                        "method": "POST",
                        "name": "CreateMenu",
                        "description": "添加菜单",
                        "mark": "add_menu",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Menu/QueryMenuByParam",
                        "method": "POST",
                        "name": "QueryMenuByParam",
                        "description": "获取菜单列表",
                        "mark": "list_menu",
                        "forbid": True
                    },
                    {
                        "path": "/v1/Menu/ModifyMenu",
                        "method": "POST",
                        "name": "ModifyMenu",
                        "description": "修改菜单信息",
                        "mark": "set_menu",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Menu/DelMenu",
                        "method": "POST",
                        "name": "DelMenu",
                        "description": "删除菜单",
                        "mark": "del_menu",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Menu/GetMenuToInterface",
                        "method": "GET",
                        "name": "GetMenuToInterface",
                        "description": "获取菜单下级联的API接口",
                        "mark": "interface_menu",
                        "forbid": False
                    }
                ]
            },
            {
                "title": "接口管理",
                "path": "/system/interface",
                "icon": "send",
                "mark": "system_interface",
                'name': 'InterfacePage',
                'component': 'interface',
                'componentPath': 'sys/interface/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Interface/CreateInterface",
                        "method": "POST",
                        "name": "CreateInterface",
                        "description": "添加接口",
                        "mark": "add_interface",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Interface/QueryInterfaceByParam",
                        "method": "POST",
                        "name": "QueryInterfaceByParam",
                        "description": "获取接口列表",
                        "mark": "list_interface",
                        "forbid": True
                    },
                    {
                        "path": "/v1/Interface/ModifyInterface",
                        "method": "POST",
                        "name": "ModifyInterface",
                        "description": "修改接口信息",
                        "mark": "set_interface",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Interface/LockInterface",
                        "method": "POST",
                        "name": "LockInterface",
                        "description": "禁用接口",
                        "mark": "lock_interface",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Interface/DelInterface",
                        "method": "POST",
                        "name": "DelInterface",
                        "description": "删除接口",
                        "mark": "del_interface",
                        "forbid": False
                    }
                ]
            },
            {
                "title": "附件管理",
                "path": "/system/document",
                "icon": "folder-open-o",
                "mark": "system_file",
                'name': 'DocumentPage',
                'component': 'document',
                'componentPath': 'sys/document/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Document/CreateDocument",
                        "method": "POST",
                        "name": "CreateDocument",
                        "description": "添加附件",
                        "mark": "add_document",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Document/QueryDocumentByParam",
                        "method": "POST",
                        "name": "QueryDocumentByParam",
                        "description": "获取附件列表",
                        "mark": "list_document",
                        "forbid": True
                    },
                    {
                        "path": "/v1/Document/DownDocument",
                        "method": "GET",
                        "name": "DownDocument",
                        "description": "下载附件",
                        "mark": "down_document",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Document/DelDocument",
                        "method": "POST",
                        "name": "DelDocument",
                        "description": "删除附件",
                        "mark": "del_document",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Document/RetrieveDocument",
                        "method": "POST",
                        "name": "RetrieveDocument",
                        "description": "回收附件",
                        "mark": "retrieve_document",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Folder/CreateFolder",
                        "method": "POST",
                        "name": "CreateFolder",
                        "description": "创建文件夹",
                        "mark": "addf_folder",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Folder/DelFolder",
                        "method": "POST",
                        "name": "DelFolder",
                        "description": "删除文件夹",
                        "mark": "delf_folder",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Folder/ModifyFolder",
                        "method": "POST",
                        "name": "ModifyFolder",
                        "description": "修改文件夹",
                        "mark": "setf_folder",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Folder/QueryFolderByParam",
                        "method": "POST",
                        "name": "QueryFolderByParam",
                        "description": "获取文件列表",
                        "mark": "listf_folder",
                        "forbid": True
                    }
                ]
            },
            {
                "title": "数据库管理",
                "path": "/system/base",
                "icon": "database",
                "mark": "system_base",
                'name': 'BasePage',
                'component': 'base',
                'componentPath': 'sys/base/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Base/ExportSql",
                        "method": "POST",
                        "name": "ExportSql",
                        "description": "导出数据库",
                        "mark": "export_sql",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Base/GetLoginInfo",
                        "method": "POST",
                        "name": "GetLoginInfo",
                        "description": "获取用户登录情况",
                        "mark": "get_login_info",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Base/GetAllUserLoginCount",
                        "method": "POST",
                        "name": "GetAllUserLoginCount",
                        "description": "获取所有用户登录次数",
                        "mark": "get_all_user_login_count",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Base/GetUserLoginIp",
                        "method": "POST",
                        "name": "GetUserLoginIp",
                        "description": "获取用户登录IP分布情况",
                        "mark": "get_user_ip",
                        "forbid": False
                    }
                ]
            }
        ]
    },
    {
        "title": "权限",
        "path": "/role",
        "icon": "shield",
        "mark": "role",
        'name': 'Role',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'cache': True,
        "children": [
            {
                "title": "管理员用户",
                "path": "/role/admin",
                "icon": "user",
                "mark": "role_admin",
                'name': 'AdminPage',
                'component': 'admin',
                'componentPath': 'sys/admin/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Admin/CreateAdmin",
                        "method": "POST",
                        "name": "CreateAdmin",
                        "description": "注册管理员",
                        "mark": "add_admin",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Admin/QueryAdminByParam",
                        "method": "POST",
                        "name": "QueryAdminByParam",
                        "description": "获取管理员列表",
                        "mark": "list_admin",
                        "forbid": True
                    },
                    {
                        "path": "/v1/Admin/ModifyAdmin",
                        "method": "POST",
                        "name": "ModifyAdmin",
                        "description": "修改管理员信息",
                        "mark": "set_admin",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Admin/LockAdmin",
                        "method": "POST",
                        "name": "LockAdmin",
                        "description": "禁用管理员",
                        "mark": "lock_admin",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Admin/DelAdmin",
                        "method": "POST",
                        "name": "DelAdmin",
                        "description": "删除管理员",
                        "mark": "del_admin",
                        "forbid": False
                    }
                ]
            },
            {
                "title": "角色管理",
                "path": "/role/role",
                "icon": "group",
                "mark": "role_group",
                'name': 'RolePage',
                'component': 'role',
                'componentPath': 'sys/role/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Role/CreateRole",
                        "method": "POST",
                        "name": "CreateRole",
                        "description": "添加角色",
                        "mark": "add_role",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Role/QueryRoleByParam",
                        "method": "POST",
                        "name": "QueryRoleByParam",
                        "description": "获取角色列表",
                        "mark": "list_role",
                        "forbid": True
                    },
                    {
                        "path": "/v1/Role/ModifyRole",
                        "method": "POST",
                        "name": "ModifyRole",
                        "description": "修改角色信息",
                        "mark": "set_role",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Role/LockRole",
                        "method": "POST",
                        "name": "LockRole",
                        "description": "禁用角色",
                        "mark": "lock_role",
                        "forbid": False
                    },
                    {
                        "path": "/v1/Role/DelRole",
                        "method": "POST",
                        "name": "DelRole",
                        "description": "删除角色",
                        "mark": "del_role",
                        "forbid": False
                    }
                ]
            }
        ]
    },
    {
        "title": "日志",
        "path": "/log",
        "icon": "bullseye",
        "mark": "log",
        'name': 'Log',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'cache': True,
        "children": [
            {
                "title": "登录日志",
                "path": "/log/login",
                "icon": "street-view",
                "mark": "log_login",
                'name': 'LogLogin',
                'component': 'login',
                'componentPath': 'sys/login/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Log/QueryLogByParam",
                        "method": "POST",
                        "name": "QueryLogByParam",
                        "description": "获取日志列表",
                        "mark": "get_log_list",
                        "forbid": True
                    }
                ]
            },
            {
                "title": "操作日志",
                "path": "/log/hander",
                "mark": "log_hander",
                "icon": "dot-circle-o",
                'name': 'LogHander',
                'component': 'hander',
                'componentPath': 'sys/hander/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Log/QueryLogByParam",
                        "method": "POST",
                        "name": "QueryLogByParam",
                        "description": "获取日志列表",
                        "mark": "get_log_list",
                        "forbid": True
                    }
                ]
            },
            {
                "title": "异常日志",
                "path": "/log/error",
                "mark": "log_error",
                "icon": "bug",
                'name': 'LorError',
                'component': 'error',
                'componentPath': 'sys/error/index',
                'cache': True,
                "interface": [
                    {
                        "path": "/v1/Log/QueryLogByParam",
                        "method": "POST",
                        "name": "QueryLogByParam",
                        "description": "获取日志列表",
                        "mark": "get_log_list",
                        "forbid": True
                    }
                ]
            }
        ]
    }
]


# 默认判断字段
default = {
    'role_mark': u'SYS_ADMIN'
}


class Config():
    def __init__(self):
        # mysql 配置信息
        self.host = '127.0.0.1'
        self.charset = 'utf8'
        if isWindows():
            self.port = 3306
            self.admin = 'root'
            self.password = 'intersky'
            self.db = 'flask'
        else:
            self.port = 3306
            self.admin = 'admin_zpp'
            self.password = 'Zt931210'
            self.db = 'admin'

    def get_sql_url(self):
        return "mysql://%s:%s@%s:%s/%s?charset=utf8" % (self.admin, self.password, self.host, self.port, self.db)

    def get_md5(self, m):
        h = hashlib.md5()
        h.update(m.encode('utf-8'))
        return h.hexdigest()


_config = Config()
