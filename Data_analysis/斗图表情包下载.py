import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os  # 这个是用于文件目录操作
from lxml import etree

url = 'https://www.doutula.com/photo/list/?page={}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

# 构建网页lists
def get_pages():
    urllists = []
    for i in range(1,10):
        urllists.append(url.format(i))
    return urllists

# 解析网页，获取目标元素
def parse_html(url):
    lists = []
    res = requests.get(url, headers=headers)
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

        #返回元组列表
        lists.append((img_links,img_names))
    return lists

# 下载图片
def download(img_link, img_name):  # 我们需要传入两个参数，图片地址，图片名称
    if os.path.exists(img_name) == False:  # 如果文件不存在，创建文件，避免重复下载
        urlretrieve(img_link, 'images/' + img_name)  # 从img_link这个网址获取文件，存储到img_name的这个文件名中去，注意要手动加上后缀
    else:
        pass

def main():
    # 1.获取所有页面的链接
    page_urllists = get_pages()

    # 2.循环解析网页、下载图片
    for url in page_urllists:
        # print(url)
        lis = parse_html(url)
        for i in lis:
            img_link, img_name = i  # 元组解包
            download(img_link, img_name)

if __name__ == '__main__':
    main()