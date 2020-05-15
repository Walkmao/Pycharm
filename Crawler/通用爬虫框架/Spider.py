# -----5.爬虫调度----------#
from firstSpider import Urlmanager
from firstSpider import Htmldownloader
from firstSpider import Htmlparse
from firstSpider import Savedata

import time

class Spider(object):
    def __init__(self):
        self.manager = Urlmanager()
        self.downloader = Htmldownloader()
        self.parse = Htmlparse()
        self.saver = Savedata()

    def Crawl(self, root_url):
        # 1.构建循环爬取的所有页面链接
        urllists = []
        for i in range(1, 2):
            urllists.append(root_url.format(i))

        # 2.从每页网址中爬取目标网址并加入到集合new_urls
        for url in urllists:
            html_cont = self.downloader.download(url)
            new_urls = self.parse.get_new_urls(html_cont)
            self.manager.add_new_urls(new_urls)

        # 3.开始不重复循环抓取目标详情页数据并保存
        while self.manager.has_new_url():
            try:
                print(len(self.manager.new_urls))  # 打印当前未爬取集合的网址个数
                new_url = self.manager.get_new_url()  # 从新集合获取一个未爬取的链接
                html_cont = self.downloader.download(new_url)  # 请求网址并返回解码后的content
                data = self.parse.get_new_data(new_url, html_cont)  # 解析网页并返回字典类型数据
                self.saver.save_data(data)  # 数据累加存储
            except Exception as e:
                print(e)
        self.saver.out_datas()

if __name__ == '__main__':
    spider_man = Spider()
    start_time = time.time()
    spider_man.Crawl("https://su.lianjia.com/ershoufang/pg{}")
    print('一共用时：', time.time() - start_time)