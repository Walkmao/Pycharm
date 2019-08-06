#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:mirco
# datetime:2019/6/20 20:45
# software: PyCharm

import requests
from bs4 import BeautifulSoup
import pandas as pd
import jieba

url_html = 'https://api.bilibili.com/x/v1/dm/list.so?oid='
url_xml = 'https://comment.bilibili.com/92542241.xml'
cid = ['92542241','98057956','94307168']

def get_data(urli):
    ri = requests.get(url = urli)
    ri.encoding = 'utf8'
    soupi = BeautifulSoup(ri.text,'lxml')
    dsi = soupi.find_all('d')
    datalst = []

    for i in dsi:
        dic = {}    #为何要放在循环体里面
        dic['弹幕'] = i.text
        datalst.append(dic)
    return datalst

#def word_count(datai):


def main():
    datai = []
    n = 0
    for id in cid:
        datai.append(get_data(url_html + id))
        print('成功采集第%i段视频' % len(datai))
        df = pd.DataFrame(datai[n])
        # 词频分析
        df['字数'] = df['弹幕'].str.len()
        df.sort_values(by='字数', ascending=False, inplace=True)
        df.head()
        n = n + 1
        print(df)
        #print('------------------------')

if __name__ == '__main__':
    main()
