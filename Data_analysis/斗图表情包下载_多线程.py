import requests
import re
from urllib.request import urlretrieve
import os
from lxml import etree
import threading
from queue import Queue

class Producer(threading.Thread):

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)   # 利用super()特殊方法调用父类的方法__init__，包含父类的属性
        # 以下为自有的属性，不用传给父类
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_html(url)

    def parse_html(self,url):
        res = requests.get(url, headers=self.headers)
        html = etree.HTML(res.text)
        # result=etree.tostring(html)
        page_links = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for page in page_links:
            img_links = page.get('data-original')
            alt = page.get('alt')

            # 字符串处理，替换中文符号
            name = re.sub(r'[\.\?？。，！,!]', '', alt)
            suffix = img_links.split('.')[-1]
            img_names = name + '.' + suffix

            self.img_queue.put((img_links,img_names))
            print(img_names,'下载完成！')

# 生产者获取图片链接并下载
class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.img_queue = img_queue
        self.page_queue = page_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            img_link, img_name = self.img_queue.get()
            self.download(img_link,img_name)

    def download(self,img_link, img_name):  # 我们需要传入两个参数，图片地址，图片名称
        if os.path.exists(img_name) == False:  # 如果文件不存在，创建文件，避免重复下载
            urlretrieve(img_link, 'images/' + img_name)  # 从img_link这个网址获取文件，存储到img_name的这个文件名中去，注意要手动加上后缀
        else:
            pass

def main():
    # 生产者生成url
    page_queue = Queue(100)
    img_queue = Queue(10000)

    url = 'https://www.doutula.com/photo/list/?page={}'
    for i in range(1, 10):
        page_queue.put(url.format(i))

    for x in range(5):
        t1 = Producer(page_queue,img_queue)
        t1.start()

    for x in range(5):
        t2 = Consumer(page_queue,img_queue)
        t2.start()

if __name__ == '__main__':
    main()