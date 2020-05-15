
'''
# 基础爬虫框架
1.URL管理

2.HTML下载

3.HTML解析

4.数据存储

5.爬虫调度
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

# -----1.URL管理------------#
class Urlmanager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取的url集合
        self.old_urls = set()  # 已爬取的url集合

    # 新集合大小
    def new_url_size(self):
        return len(self.new_urls)

    # 判断是否还有新的url
    def has_new_url(self):
        return self.new_url_size() != 0

    # 从未爬取的的集合获取一个url
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    # 添加单个url，并去重
    def add_new_url(self, url):
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 将新的url添加到未爬取的url集合中
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)


# -----2.HTML下载-----------#
class Htmldownloader(object):
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }
        self.cookies = None

    def download(self, url):
        response = requests.get(url, headers=self.headers)
        # status = r.status_code
        try:
            return response.content.decode()
        except Exception as e:
            print('请求错误：', e)


# -----3.HTML解析-----------#
class Htmlparse(object):
    # 解析页面网址获取新的网址并添加到此集合中
    def get_new_urls(self, html_cont):
        new_urls = set()
        soup = BeautifulSoup(html_cont, 'lxml')
        urls = soup.find_all('a', class_="noresultRecommend img LOGCLICKDATA")
        for i in urls:
            new_urls.add(i["href"])
        return new_urls

    # 解析详情页网站获取数据
    def get_new_data(self, page_url, html_cont):
        soup = BeautifulSoup(html_cont, 'lxml')
        dic_data = {}

        # 用户自定义区域：根据实际需求进行自定义修改
        dic_data['url'] = page_url

        dic_data['title'] = soup.select('.main')[0].text

        dic_data['price'] = soup.select('.total')[0].text + '万'
        # 单价
        dic_data['unitPrice'] = soup.select('.unitPrice')[0].text
        # 户型
        dic_data['room'] = soup.select('.room')[0].text
        # 朝向
        dic_data['type'] = soup.select('.type')[0].text
        # 面积
        dic_data['area'] = soup.select('.area')[0].text[:7]
        # 小区名称
        dic_data['communityName'] = soup.select('.communityName')[0].text[4:-2]

        return dic_data


# -----4.数据存储-----------#
class Savedata(object):

    def __init__(self):
        self.datas = []

    def save_data(self, data):
        self.datas.append(data)

    def out_datas(self):
        pd_datas = pd.DataFrame(self.datas)
        # columns字段：自定义列的顺序（DataFrame默认按列名的字典序排序）
        # columns = ["小区", "户型", "面积", "价格", "单价", "朝向", "电梯", "位置", "地铁"]
        pd_datas.to_csv(r"C:\Users\Mirco\Desktop\Lianjia.csv", encoding='utf_8_sig', index=False)

