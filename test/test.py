#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 测试脚本
@Author: Zpp
@Date: 2020-04-24 14:55:37
@LastEditors: Zpp
@LastEditTime: 2020-05-25 15:42:47
'''


if __name__ == '__main__':
    import geoip2.database
    import os

    root = os.path.abspath(os.path.dirname(__file__) + '/..')

    reader = geoip2.database.Reader(os.path.join(root, 'tools/GeoLite2-City.mmdb'))

    response = reader.city('116.234.9.196')
    print response.continent.names["zh-CN"]
    print response.country.names["zh-CN"]
    print response.subdivisions.most_specific.names["zh-CN"]
    print response.city.names["zh-CN"]
    print response.location.longitude
    print response.location.latitude
