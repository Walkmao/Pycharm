#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:mirco
# datetime:2019/9/24 11:47
# software: PyCharm

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from fake_useragent import UserAgent
import time

# def __init__(self):
#     self.headers = {"User-Agent": UserAgent().random}
#     self.datas = list()

headers = {"User-Agent": UserAgent().random}

# 获取网页的最大页码totalpage
def total_pages(url):
    res = requests.get(url,headers = headers)
    if res.status_code == 200:
        soup = bs(res.text,'lxml')
        page = soup.find('div',class_="page-box house-lst-page-box")
        total_page = eval(page["page-data"])['totalPage']
        return total_page
    else:
        print("fail stautus:{}".format(res.status_code))
        return None

# 生成所有页面的网址url
def generate_ulr(url,n):
    urlist = []
    for i in range(1,n+1):
        urli = url % i
        urlist.append(urli)
    return urlist

#获取每一页的详情页url
def get_url(generate_url):
    urlslist = []
    res = requests.get(generate_url,headers = headers)
    soup = bs(res.text,'lxml')
    urls = soup.find_all('a',class_ ="noresultRecommend img LOGCLICKDATA")
    for i in urls:
        urlslist.append(i["href"])
    return urlslist

def open_url(get_url):
    res = requests.get(get_url, headers = headers)
    dic = {}
    if res.status_code == 200:
        soup = bs(res.text, 'lxml')
        # -----------select-----------------
        # title 标题
        dic['title'] = soup.select('.main')[0].text
        # soup.select('.main')，因为这里是一个class，所以前面要加.，如果筛选的是id，则加#。
        # Prince 总价
        dic['price'] = soup.select('.total')[0].text + '万'
        # 单价
        dic['unitPrice'] = soup.select('.unitPrice')[0].text
        # 户型
        dic['room'] = soup.select('.room')[0].text
        # 朝向
        dic['type'] = soup.select('.type')[0].text
        # 面积
        dic['area'] = soup.select('.area')[0].text[:7]
        # 小区名称
        dic['communityName'] = soup.select('.communityName')[0].text[4:-2]
        # 面积
        dic['areaName'] = soup.select('.areaName')[0].text[4:]
        # 房屋编号
        dic['houseRecord'] = soup.select('.houseRecord')[0].text[4:16]
        # -----------find-------------------
        # ul = soup.find('div', class_="base").find('ul')   #获取包含当前页面信息list的块，并返回字符串类型
        li = soup.find('div', class_="base").find('ul').find_all('li')  # 从ul块下钻到li每个景点list,并返回对象是列表
        dic['房屋户型'] = li[0].text[4:]
        dic['所在楼层'] = li[1].text[4:]
        dic['建筑面积'] = li[2].text[4:]
        dic['产权年限'] = li[11].text[4:]

        ul2 = soup.find('div', class_="area").find('div', class_="subInfo")
        dic['年建'] = ul2.text
        return dic
    else:
        return None

def pandas_to_xlsx(info):
    pd_look = pd.DataFrame(info)
    pd_look.to_excel('链家二手房.xlsx',sheet_name='链家二手房')

def main():
    rurl = 'https://su.lianjia.com/ershoufang/'
    rurl1 = 'https://su.lianjia.com/ershoufang/pg%s'

    page_n = total_pages(rurl)  #获取最大页数
    page_urllist = generate_ulr(rurl1,2)  #生成所有页面链接列表

    urllist = []   #获取每个页面中30个块详情页链接
    for p in page_urllist:
        urli = get_url(p)
        urllist.extend(urli)

    data = []
    for i in urllist:
        try:
            data.append(open_url(i))
            time.sleep(1)
            print('成功采集%i' % len(data))
        except Exception as e:
            print(e)

    # pd_look = pd.DataFrame(data)
    # print (pd_look)
    pandas_to_xlsx(data)

if __name__ == '__main__':
    main()