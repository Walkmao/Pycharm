# -*- coding:utf-8 -*-
from __future__ import unicode_literals


import requests
import pandas as pd
import time
import sys


def parse():
    total_data = pd.read_csv('begin.csv', header=1)
    total_list_data = total_data['123456']
    return total_list_data


def search_location(address):
    params = {'address': address,
              'city': '苏州',
              'key': '请写入你自己的key'}
    base_url = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(url=base_url, params=params)
    json_data = response.json()
    if json_data['status'] == '1' and len(json_data['geocodes']) > 0:
        return json_data['geocodes'][0]['location'] if json_data['geocodes'][0]['location'] else 'errorlocation', json_data
    return 'errorlocation', json_data


def search_address_detail(location):
    params = {'location': location,
              'key': '写入你的key'}
    base_url = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(url=base_url, params=params)
    json_data = response.json()
    if json_data['status'] == '1':
        if json_data['regeocode']['addressComponent']['township']:
            return json_data['regeocode']['addressComponent']['township'], json_data
    return 'errorSearchAddress', json_data


if __name__ == '__main__':
    df = pd.DataFrame(columns=['originAddress', 'location', 'anotherInfo', 'searchTownship', 'searchAnotherAddress'])
    address_list = parse()
    index = 0
    for address in address_list:
        # 地址,处理坑爹数据
        address_deal = address.split(' ',1)
        real_address = ''
        for real in address_deal:
            if len(real) > len(real_address):
                real_address = real
        # 搜索location
        location_str, search_json = search_location(address=real_address)
        # 利用location搜索township
        township_str, search_address_json = search_address_detail(location=location_str)
        df.loc[index] = [address, location_str, search_json, township_str, search_address_json]
        index = index + 1
        print('正在查询')
        print(index)
    df.to_csv('locationDetail.csv', index=True)
    print('输出csv成功')