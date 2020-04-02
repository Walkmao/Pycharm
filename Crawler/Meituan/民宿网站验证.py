import requests
from bs4 import BeautifulSoup

class Spider:
    def __init__(self):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.366'}
        #self.name = name
        # self.url = url
        # self.url_temp = 'https://tieba.baidu.com/f?kw='+name+'pn={}'

    def get_url_list(self):
        url_list = []
        for i in range(100):
            url_list.append(self.url_temp.format(i*50))  # 一页50条数据，+50翻一页
        return url_list
        # return [self.url_temp.format(i*50) for i in range(100)]

    def get_response(self,url):
        # print(url)
        res = requests.get(url,headers=self.headers)
        print(res.url)
        print(res.status_code,res.apparent_encoding,res.content.decode())
        return res.content.decode()

    def save_result(self,html_str,page_num):
        file_path = '{}-第{}页.html'.format(self.tieba_name,page_num)
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(html_str)

    def run(self):
        # 1.构造url列表
        url_list = self.get_url_list()

        # 2.遍历，发送请求，获取响应
        for url in url_list:
            html_str = self.get_response(url)

        # 3.数据存储
        page_num = url_list.index(url) + 1
        self.save_result(html_str,page_num)

if __name__ == '__main__':
    re_url = 'https://www.airbnb.cn/s/%E8%8B%8F%E5%B7%9E/homes?place_id=ChIJF0RJ1CunszURLncfnJpFsSc&map_toggle=false'
    min_su = Spider()
    min_su.get_response(re_url)