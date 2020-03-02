#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 基本配置信息
@Author: Zpp
@Date: 2019-09-02 15:53:39
@LastEditTime: 2020-03-02 16:58:30
@LastEditors: Zpp
'''
import hashlib
import os

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')

base_info = {
    'lock_times': 5, # 开始锁定的次数
    'lock_every_time': 5 # 超过锁定次数每次加的时间
}

token_info = {
    'expiration': 30 * 24 * 3600,
    'SECRET_KEY': 'k#6@1%8)a'
}

# 启动服务参数 字典类型
server_info = {
    "host": '0.0.0.0',
    "port": 91,  # 启动服务的端口号
}

# 文档路径
document_dir = os.path.join(basedir, 'document')

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
    'SESSION_FILE_MODE': 384
}

# cache参数
cache_info = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': os.path.join(basedir, 'caches'),
    'CACHE_THRESHOLD': 500
}

# 初始化路由配置
init_route = [
    {
        'name': 'System',
        'path': '/system',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'title': u'系统设置',
        'cache': True,
        'children': [
            {
                'name': 'MenuPage',
                'path': '/system/menu',
                'component': 'menu',
                'componentPath': 'sys/menu/index',
                'title': u'菜单管理',
                'cache': True
            },
            {
                'name': 'RoutePage',
                'path': '/system/route',
                'component': 'route',
                'componentPath': 'sys/route/index',
                'title': u'路由管理',
                'cache': True
            },
            {
                'name': 'InterfacePage',
                'path': '/system/interface',
                'component': 'interface',
                'componentPath': 'sys/interface/index',
                'title': u'接口管理',
                'cache': True
            },
            {
                'name': 'DocumentPage',
                'path': '/system/document',
                'component': 'document',
                'componentPath': 'sys/document/index',
                'title': u'附件管理',
                'cache': True
            },
            {
                'name': 'BasePage',
                'path': '/system/base',
                'component': 'base',
                'componentPath': 'sys/base/index',
                'title': u'数据库管理',
                'cache': True
            }
        ]
    },
    {
        'name': 'Role',
        'path': '/role',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'title': u'权限管理',
        'cache': True,
        'children': [
            {
                'name': 'AdminPage',
                'path': '/role/admin',
                'component': 'admin',
                'componentPath': 'sys/admin/index',
                'title': u'管理员用户',
                'cache': True
            },
            {
                'name': 'RolePage',
                'path': '/role/role',
                'component': 'role',
                'componentPath': 'sys/role/index',
                'title': u'角色管理',
                'cache': True
            }
        ]
    },
    {
        'name': 'Log',
        'path': '/log',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside',
        'title': u'日志管理',
        'cache': True,
        'children': [
            {
                'name': 'LogLogin',
                'path': '/log/login',
                'component': 'login',
                'componentPath': 'sys/login/index',
                'title': u'登录日志',
                'cache': True
            },
            {
                'name': 'LogHander',
                'path': '/log/hander',
                'component': 'hander',
                'componentPath': 'sys/hander/index',
                'title': u'操作日志',
                'cache': True
            },
            {
                'name': 'LorError',
                'path': '/log/error',
                'component': 'error',
                'componentPath': 'sys/error/index',
                'title': u'异常日志',
                'cache': True
            }
        ]
    }
]

# 初始化菜单和下属的接口
init_menu = [
    {
        "title": "系统",
        "path": "/system",
        "icon": "cog",
        "mark": "system",
        "children": [
            {
                "title": "菜单管理",
                "path": "/system/menu",
                "icon": "th-list",
                "mark": "system_menu",
                "interface": [
                    {
                        "path": "/v1/Menu/CreateMenu",
                        "method": "POST",
                        "name": "CreateMenu",
                        "description": "添加菜单",
                        "mark": "add_menu",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Menu/QueryMenuByParam",
                        "method": "POST",
                        "name": "QueryMenuByParam",
                        "description": "获取菜单列表",
                        "mark": "get_menu_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Menu/ModifyMenu",
                        "method": "POST",
                        "name": "ModifyMenu",
                        "description": "修改菜单信息",
                        "mark": "set_menu",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Menu/LockMenu",
                        "method": "POST",
                        "name": "LockMenu",
                        "description": "禁用菜单",
                        "mark": "lock_menu",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Menu/DelMenu",
                        "method": "POST",
                        "name": "DelMenu",
                        "description": "删除菜单",
                        "mark": "del_menu",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Menu/GetMenuToInterface",
                        "method": "GET",
                        "name": "GetMenuToInterface",
                        "description": "获取菜单下级联的API接口",
                        "mark": "get_menu_to_interface",
                        "not_allow": False
                    }
                ]
            },
            {
                "title": "路由管理",
                "path": "/system/route",
                "icon": "share-alt",
                "mark": "system_route",
                "interface": [
                    {
                        "path": "/v1/Route/CreateRoute",
                        "method": "POST",
                        "name": "CreateRoute",
                        "description": "添加路由",
                        "mark": "add_router",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Route/QueryRouteByParam",
                        "method": "POST",
                        "name": "QueryRouteByParam",
                        "description": "获取路由列表",
                        "mark": "get_router_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Route/ModifyRoute",
                        "method": "POST",
                        "name": "ModifyRoute",
                        "description": "修改路由信息",
                        "mark": "set_router",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Route/LockRoute",
                        "method": "POST",
                        "name": "LockRoute",
                        "description": "禁用路由",
                        "mark": "lock_router",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Route/DelRoute",
                        "method": "POST",
                        "name": "DelRoute",
                        "description": "删除路由",
                        "mark": "del_router",
                        "not_allow": False
                    }
                ]
            },
            {
                "title": "接口管理",
                "path": "/system/interface",
                "icon": "send",
                "mark": "system_interface",
                "interface": [
                    {
                        "path": "/v1/Interface/CreateInterface",
                        "method": "POST",
                        "name": "CreateInterface",
                        "description": "添加接口",
                        "mark": "add_interface",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Interface/QueryInterfaceByParam",
                        "method": "POST",
                        "name": "QueryInterfaceByParam",
                        "description": "获取接口列表",
                        "mark": "get_interface_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Interface/ModifyInterface",
                        "method": "POST",
                        "name": "ModifyInterface",
                        "description": "修改接口信息",
                        "mark": "set_interface",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Interface/LockInterface",
                        "method": "POST",
                        "name": "LockInterface",
                        "description": "禁用接口",
                        "mark": "lock_interface",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Interface/DelInterface",
                        "method": "POST",
                        "name": "DelInterface",
                        "description": "删除接口",
                        "mark": "del_interface",
                        "not_allow": False
                    }
                ]
            },
            {
                "title": "附件管理",
                "path": "/system/document",
                "icon": "folder-open-o",
                "mark": "system_file",
                "interface": [
                    {
                        "path": "/v1/Document/CreateDocument",
                        "method": "POST",
                        "name": "CreateDocument",
                        "description": "添加附件",
                        "mark": "add_document",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Document/QueryDocumentByParam",
                        "method": "POST",
                        "name": "QueryDocumentByParam",
                        "description": "获取附件列表",
                        "mark": "get_document_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Document/DownDocument",
                        "method": "GET",
                        "name": "DownDocument",
                        "description": "下载附件",
                        "mark": "down_document",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Document/DelDocument",
                        "method": "POST",
                        "name": "DelDocument",
                        "description": "删除附件",
                        "mark": "del_document",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Document/RetrieveDocument",
                        "method": "POST",
                        "name": "RetrieveDocument",
                        "description": "回收附件",
                        "mark": "retrieve_document",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Folder/CreateFolder",
                        "method": "POST",
                        "name": "CreateFolder",
                        "description": "创建文件夹",
                        "mark": "create_folder",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Folder/DelFolder",
                        "method": "POST",
                        "name": "DelFolder",
                        "description": "删除文件夹",
                        "mark": "del_folder",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Folder/ModifyFolder",
                        "method": "POST",
                        "name": "ModifyFolder",
                        "description": "修改文件夹",
                        "mark": "modify_folder",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Folder/QueryFolderByParam",
                        "method": "POST",
                        "name": "QueryFolderByParam",
                        "description": "获取附件列表",
                        "mark": "query_folder",
                        "not_allow": True
                    }
                ]
            },
            {
                "title": "数据库管理",
                "path": "/system/base",
                "icon": "database",
                "mark": "system_base",
                "interface": [
                    {
                        "path": "/v1/Base/ExportSql",
                        "method": "POST",
                        "name": "ExportSql",
                        "description": "导出数据库",
                        "mark": "export_sql",
                        "not_allow": False
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
        "children": [
            {
                "title": "管理员用户",
                "path": "/role/admin",
                "icon": "user",
                "mark": "role_admin",
                "interface": [
                    {
                        "path": "/v1/Admin/CreateAdmin",
                        "method": "POST",
                        "name": "CreateAdmin",
                        "description": "注册管理员",
                        "mark": "add_admin",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Admin/QueryAdminByParam",
                        "method": "POST",
                        "name": "QueryAdminByParam",
                        "description": "获取管理员列表",
                        "mark": "get_admin_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Admin/ModifyAdmin",
                        "method": "POST",
                        "name": "ModifyAdmin",
                        "description": "修改管理员信息",
                        "mark": "set_admin",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Admin/LockAdmin",
                        "method": "POST",
                        "name": "LockAdmin",
                        "description": "禁用管理员",
                        "mark": "lock_admin",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Admin/DelAdmin",
                        "method": "POST",
                        "name": "DelAdmin",
                        "description": "删除管理员",
                        "mark": "del_admin",
                        "not_allow": False
                    }
                ]
            },
            {
                "title": "角色管理",
                "path": "/role/role",
                "icon": "group",
                "mark": "role_group",
                "interface": [
                    {
                        "path": "/v1/Role/CreateRole",
                        "method": "POST",
                        "name": "CreateRole",
                        "description": "添加角色",
                        "mark": "add_role",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Role/QueryRoleByParam",
                        "method": "POST",
                        "name": "QueryRoleByParam",
                        "description": "获取角色列表",
                        "mark": "get_role_list",
                        "not_allow": True
                    },
                    {
                        "path": "/v1/Role/ModifyRole",
                        "method": "POST",
                        "name": "ModifyRole",
                        "description": "修改角色信息",
                        "mark": "set_role",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Role/LockRole",
                        "method": "POST",
                        "name": "LockRole",
                        "description": "禁用角色",
                        "mark": "lock_role",
                        "not_allow": False
                    },
                    {
                        "path": "/v1/Role/DelRole",
                        "method": "POST",
                        "name": "DelRole",
                        "description": "删除角色",
                        "mark": "del_role",
                        "not_allow": False
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
        "interface": [
            {
                "path": "/v1/Log/QueryLogByParam",
                "method": "POST",
                "name": "QueryLogByParam",
                "description": "获取日志列表",
                "mark": "get_log_list",
                "not_allow": True
            }
        ],
        "children": [
            {
                "title": "登录日志",
                "path": "/log/login",
                "icon": "street-view",
                "mark": "log_login"
            },
            {
                "title": "操作日志",
                "path": "/log/hander",
                "mark": "log_hander",
                "icon": "dot-circle-o"
            },
            {
                "title": "异常日志",
                "path": "/log/error",
                "mark": "log_error",
                "icon": "bug"
            }
        ]
    }
]


class Config():
    def __init__(self):
        # mysql 配置信息
        self.host = '127.0.0.1'
        self.port = 3306
        self.admin = 'flask_user'
        self.password = 'intersky'
        self.db = 'flask'
        self.charset = 'utf8'

    def get_sql_url(self):
        return "mysql://%s:%s@%s:%s/%s?charset=utf8" % (self.admin, self.password, self.host, self.port, self.db)

    def get_md5(self, m):
        h = hashlib.md5()
        h.update(m.encode('utf-8'))
        return h.hexdigest()
