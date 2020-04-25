![默哀](https://github.com/huzidabanzhang/python-admin/blob/master/trunk/static/image/markdown/desktop.jpg "默哀")

## 演示
  https://ig132n.cn/
  
  测试账号：Test 密码：123456
  
  前端地址 [Vue](https://github.com/huzidabanzhang/python-admin-pm "Vue")
  
## 验证器
  [验证器](https://github.com/huzidabanzhang/python-admin/blob/master/trunk/validate/__init__.py "验证器")
  ```python
  {
      'name': u'手机号',  # 字段名称
      'value': 'phone',   # 字段
      'type': 'phone',    # 有int str list file files phone email time ic boolean
      'required': True,   # 是否必填
      // 'max': 99,     # 最大值 只有int str 有
      // 'min': 1,     # 最小值 只有int str 有
      // 'between': [1, 2],   # 值在list之间 只有int str 有
      // 'default': 133333333,   # 默认值
      // 'msg': u'手机号必填',     # 有msg将代替默认错误提示
  }
  ```
  
## 功能

* 管理员管理
* 菜单管理
* 路由管理
* 角色管理
* 接口管理
* 文档管理
* 数据库管理
* 日志

## 注意
  tools/manage.py为数据库版本控制的py，具体的使用介绍你可以看： [章胖胖的笔记](https://huzidabanzhang.github.io/notes/2020-03-30.html#python-flask-migrate-%E8%BF%81%E7%A7%BB%E6%95%B0%E6%8D%AE%E5%BA%93 "章胖胖的笔记")
  
  其中conf下有aliyun.py是放阿里云密钥需要自己创建
  
  新加了GeoLite2的IP转换地址

## 启动
  第一次启动前，先创建一个数据库，然后在conf/setting.py里面数据库配置修改数据库信息
  
  ```shell
  python start.py # 启动服务
  ```
  
## 计划
  加入分支开始自己的装修记录
  
  准备文档
