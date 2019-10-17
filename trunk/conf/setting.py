#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 基本配置信息
@Author: Zpp
@Date: 2019-09-02 15:53:39
@LastEditTime: 2019-10-17 16:21:00
@LastEditors: Zpp
'''
import hashlib
import os

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')

token_info = {
    'expiration': 30 * 24 * 3600,
    'SECRET_KEY': 'k#6@1%8)a'
}

# 启动服务参数 字典类型
server_info = {
    "host": '0.0.0.0',
    "port": 5000,  # 启动服务的端口号
}

# 文档路径
document_dir = os.path.join(basedir, 'document')

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
        'componentPath': 'layout/header-aside/layout',
        'title': u'系统设置',
        'cache': True,
        'children': [
            {
                'name': 'MenuPage',
                'path': '/system/menu',
                'component': 'menu',
                'componentPath': 'pages/sys/menu/index',
                'title': u'菜单管理',
                'cache': True
            },
            {
                'name': 'RoutePage',
                'path': '/system/route',
                'component': 'route',
                'componentPath': 'pages/sys/route/index',
                'title': u'路由管理',
                'cache': True
            },
            {
                'name': 'InterfacePage',
                'path': '/system/interface',
                'component': 'interface',
                'componentPath': 'pages/sys/interface/index',
                'title': u'接口管理',
                'cache': True
            },
            {
                'name': 'DocumentPage',
                'path': '/system/document',
                'component': 'document',
                'componentPath': 'pages/sys/document/index',
                'title': u'文档管理',
                'cache': True
            }
        ]
    },
    {
        'name': 'Role',
        'path': '/role',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside/layout',
        'title': u'权限管理',
        'cache': True,
        'children': [
            {
                'name': 'AdminPage',
                'path': '/role/admin',
                'component': 'admin',
                'componentPath': 'pages/sys/admin/index',
                'title': u'管理员用户',
                'cache': True
            },
            {
                'name': 'RolePage',
                'path': '/role/role',
                'component': 'role',
                'componentPath': 'pages/sys/role/index',
                'title': u'角色管理',
                'cache': True
            }
        ]
    },
    {
        'name': 'Log',
        'path': '/log',
        'component': 'layoutHeaderAside',
        'componentPath': 'layout/header-aside/layout',
        'title': u'日志管理',
        'cache': True,
        'children': [
            {
                'name': 'LogLogin',
                'path': '/log/login',
                'component': 'login',
                'componentPath': 'pages/sys/login/index',
                'title': u'登录日志',
                'cache': True
            },
            {
                'name': 'LogHander',
                'path': '/log/hander',
                'component': 'hander',
                'componentPath': 'pages/sys/hander/index',
                'title': u'操作日志',
                'cache': True
            },
            {
                'name': 'LorError',
                'path': '/log/error',
                'component': 'error',
                'componentPath': 'pages/sys/error/index',
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
        "children": [
            {
                "title": "菜单管理",
                "path": "/system/menu",
                "icon": "th-list",
                "interface": [
                    {
                        "path": "/v1/Menu/CreateMenu",
                        "method": "POST",
                        "name": "CreateMenu",
                        "description": "添加菜单"
                    },
                    {
                        "path": "/v1/Menu/QueryMenuByParam",
                        "method": "POST",
                        "name": "QueryMenuByParam",
                        "description": "获取菜单列表"
                    },
                    {
                        "path": "/v1/Menu/ModifyMenu",
                        "method": "POST",
                        "name": "ModifyMenu",
                        "description": "修改菜单信息"
                    },
                    {
                        "path": "/v1/Menu/LockMenu",
                        "method": "POST",
                        "name": "LockMenu",
                        "description": "禁用菜单"
                    },
                    {
                        "path": "/v1/Menu/GetMenu/:menu_id",
                        "method": "GET",
                        "name": "GetMenu",
                        "description": "根据ID获取菜单"
                    }
                ]
            },
            {
                "title": "路由管理",
                "path": "/system/route",
                "icon": "share-alt",
                "interface": [
                    {
                        "path": "/v1/Route/CreateRoute",
                        "method": "POST",
                        "name": "CreateRoute",
                        "description": "添加路由"
                    },
                    {
                        "path": "/v1/Route/QueryRouteByParam",
                        "method": "POST",
                        "name": "QueryRouteByParam",
                        "description": "获取路由列表"
                    },
                    {
                        "path": "/v1/Route/ModifyRoute",
                        "method": "POST",
                        "name": "ModifyRoute",
                        "description": "修改路由信息"
                    },
                    {
                        "path": "/v1/Route/LockRoute",
                        "method": "POST",
                        "name": "LockRoute",
                        "description": "禁用路由"
                    }
                ]
            },
            {
                "title": "接口管理",
                "path": "/system/interface",
                "icon": "send",
                "interface": [
                    {
                        "path": "/v1/Interface/CreateInterface",
                        "method": "POST",
                        "name": "CreateInterface",
                        "description": "添加接口"
                    },
                    {
                        "path": "/v1/Interface/QueryInterfaceByParam",
                        "method": "POST",
                        "name": "QueryInterfaceByParam",
                        "description": "获取接口列表"
                    },
                    {
                        "path": "/v1/Interface/ModifyInterface",
                        "method": "POST",
                        "name": "ModifyInterface",
                        "description": "修改接口信息"
                    },
                    {
                        "path": "/v1/Interface/LockInterface",
                        "method": "POST",
                        "name": "LockInterface",
                        "description": "禁用接口"
                    }
                ]
            },
            {
                "title": "文档管理",
                "path": "/system/document",
                "icon": "folder",
                "interface": [
                    {
                        "path": "/v1/Document/CreateDocument",
                        "method": "POST",
                        "name": "CreateDocument",
                        "description": "添加文档"
                    },
                    {
                        "path": "/v1/Document/QueryDocumentByParam",
                        "method": "POST",
                        "name": "QueryDocumentByParam",
                        "description": "获取文档列表"
                    },
                    {
                        "path": "/v1/Document/GetDocument/:filename",
                        "method": "GET",
                        "name": "GetDocument",
                        "description": "预览图片"
                    },
                    {
                        "path": "/v1/Document/DownDocument/:filename",
                        "method": "GET",
                        "name": "DownDocument",
                        "description": "下载文档"
                    },
                    {
                        "path": "/v1/Document/DelDocument",
                        "method": "POST",
                        "name": "DelDocument",
                        "description": "禁用文档"
                    }
                ]
            }
        ]
    },
    {
        "title": "权限",
        "path": "/role",
        "icon": "shield",
        "children": [
            {
                "title": "管理员用户",
                "path": "/role/admin",
                "icon": "user",
                "interface": [
                    {
                        "path": "/v1/Admin/CreateAdmin",
                        "method": "POST",
                        "name": "CreateAdmin",
                        "description": "注册管理员"
                    },
                    {
                        "path": "/v1/Admin/QueryAdminByParam",
                        "method": "POST",
                        "name": "QueryAdminByParam",
                        "description": "获取管理员列表"
                    },
                    {
                        "path": "/v1/Admin/ModifyAdmin",
                        "method": "POST",
                        "name": "ModifyAdmin",
                        "description": "修改管理员信息"
                    },
                    {
                        "path": "/v1/Admin/LockAdmin",
                        "method": "POST",
                        "name": "LockAdmin",
                        "description": "禁用管理员"
                    },
                    {
                        "path": "/v1/Admin/Logout",
                        "method": "GET",
                        "name": "Logout",
                        "description": "注销管理员"
                    },
                    {
                        "path": "/v1/Admin/Login",
                        "method": "POST",
                        "name": "Login",
                        "description": "管理员登录"
                    },
                    {
                        "path": "/v1/Admin/Captcha",
                        "method": "GET",
                        "name": "Captcha",
                        "description": "验证码"
                    },
                    {
                        "path": "/v1/Admin/CreateDrop",
                        "method": "GET",
                        "name": "CreateDrop",
                        "description": "初始化数据库"
                    }
                ]
            },
            {
                "title": "角色管理",
                "path": "/role/role",
                "icon": "group",
                "interface": [
                    {
                        "path": "/v1/Role/CreateRole",
                        "method": "POST",
                        "name": "CreateRole",
                        "description": "添加角色"
                    },
                    {
                        "path": "/v1/Role/QueryRoleByParam",
                        "method": "POST",
                        "name": "QueryRoleByParam",
                        "description": "获取角色列表"
                    },
                    {
                        "path": "/v1/Role/ModifyRoleToRoute",
                        "method": "POST",
                        "name": "ModifyRoleToRoute",
                        "description": "修改角色和路由关系"
                    },
                    {
                        "path": "/v1/Role/ModifyRoleToMenu",
                        "method": "POST",
                        "name": "ModifyRoleToMenu",
                        "description": "修改角色和菜单关系"
                    },
                    {
                        "path": "/v1/Role/ModifyRole",
                        "method": "POST",
                        "name": "ModifyRole",
                        "description": "修改角色信息"
                    },
                    {
                        "path": "/v1/Role/LockRole",
                        "method": "POST",
                        "name": "LockRole",
                        "description": "禁用角色"
                    }
                ]
            }
        ]
    },
    {
        "title": "日志",
        "path": "/log",
        "icon": "bullseye",
        "children": [
            {
                "title": "登录日志",
                "path": "/log/login",
                "icon": "street-view",
                "interface": [
                    {
                        "path": "/v1/Log/QueryLogByParam",
                        "method": "POST",
                        "name": "QueryLogByParam",
                        "description": "获取日志列表"
                    }
                ]
            },
            {
                "title": "操作日志",
                "path": "/log/hander",
                "icon": "dot-circle-o"
            },
            {
                "title": "异常日志",
                "path": "/log/error",
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
        self.admin = 'root'
        self.password = 'intersky'
        self.db = 'flask'
        self.charset = 'utf8'

    def get_sql_url(self):
        return "mysql://%s:%s@%s:%s/%s?charset=utf8" % (self.admin, self.password, self.host, self.port, self.db)

    def get_md5(self, m):
        h = hashlib.md5()
        h.update(m.encode('utf-8'))
        return h.hexdigest()
