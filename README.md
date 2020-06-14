## 演示

https://test.ig132n.cn/

测试账号：Test 密码：111111

前端地址 [Vue](https://github.com/huzidabanzhang/python-admin-pm "Vue")

![首页](https://github.com/huzidabanzhang/python-admin/blob/master/static/image/markdown/desktop.png "首页")

![菜单](https://github.com/huzidabanzhang/python-admin/blob/master/static/image/markdown/menu.png "菜单")

![权限](https://github.com/huzidabanzhang/python-admin/blob/master/static/image/markdown/role.png "权限")

## 验证器

[验证器](https://github.com/huzidabanzhang/python-admin/blob/master/trunk/validate/__init__.py "验证器")

```python
# 路由中引用验证器
from validate import validate_form
from validate.v1.admin import params
validate = validate_form(params)

@route_admin.route('/Login', methods=['POST'], endpoint='Login') # endpoint这个一定要加 不然报错
@validate.form('Login') # 需要验证的场景
```

```python
# 验证器路径/validate/v1中
params = {
    # 引用验证字段场景
    'Test': ['admin_id[]', 'disable'],
    # 验证场景中需要修改字段里面的内容或者增加字段内容
    # 用dict里面加入field这个很重要要判断是哪个字段dict会覆盖原来的判断条件
    'Test2': [{
        'field': 'code',
        'required': False
    }],
    # 验证字段
    'fields': {
        'code': {
            'name': u'验证码',
            'type': 'str', # 字段类型包括str, list, int, boolean, ic, phone, email, time
            'min': 4, # 字符长度最小值 其中list判断长度
            'max': 4, # 字符长度最小值 其中list判断长度
            'between': [888, 999], # 字符必须在list中
            'required': True, # 是否必填
            'default': 111  # 默认值
        },
        'email': {
            'name': u'邮件',
            'type': 'email'
        },
        'sex': {
            'name': u'性别',
            'type': 'int',
            'default': 1
        },
        'disable': {
            'name': u'可见性',
            'type': 'boolean',
            'required': True
        },
        'admin_id[]': {
            'name': u'管理员编号',
            'type': 'list',
            'required': True
        }
    }
}
```

## 功能

-   管理员管理
-   菜单管理
-   角色管理
-   接口管理
-   文档管理
-   数据库管理
-   日志查看

## 注意

tools/manage.py 为数据库版本控制的 py，具体的使用介绍你可以看： [章胖胖的笔记](https://huzidabanzhang.github.io/notes/2020-03-30.html#python-flask-migrate-%E8%BF%81%E7%A7%BB%E6%95%B0%E6%8D%AE%E5%BA%93 "章胖胖的笔记")

其中 conf 下有 aliyun.py 是放阿里云密钥需要自己创建

新加了 GeoLite2 的 IP 转换地址

## 启动

第一次启动前，先创建一个数据库，然后在目录 conf/setting.py 里面类中修改连接数据库信息

```shell
python start.py # 启动服务
```

前端页面打开第一次会提示是否初始化数据库，初始化后会提示弹出Admin的初始密码登录即可.

## 计划

无

<a href="https://github.com/d2-projects/d2-admin" target="_blank"><img src="https://raw.githubusercontent.com/FairyEver/d2-admin/master/docs/image/d2-admin@2x.png" width="200"></a>
