
import time
import json
import requests
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from mysqldatabase import database_mysql

class Crawler:
    def __init__(self):
        self.headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.366'}
        self.url = 'https://minsu.meituan.com/suzhou/h6560/'
        self.comment_url = 'https://minsu.meituan.com/gw/ugc/api/v1/product/comments?productId={}'
        #self.url = 'https://minsu.meituan.com/suzhou/h6560/?dateBegin=20200317&dateEnd=20200318' 添加日期范围
        self.conn = None
        self.cur = None
    # def __str__(self):
    #     """返回一个对象的描述信息"""
    #     # print(num)
    #     return "爬取的网址是:%s" % self.url

    def visit_site(self,url):
        r = requests.get(url,headers=self.headers)
        data = r.content.decode('utf-8')
        soup = BeautifulSoup(data,'lxml')
        return soup

    def get_page_list(self):
        soup = self.visit_site(self.url)
        max_page = int(soup.find_all('a',class_='page-link')[-2].text)
        page_list = []
        for i in range(1,max_page+1):
            li = self.url + 'pn' + str(i)
            page_list.append(li)
        return  page_list

    def get_url_list(self,url):
        soup = self.visit_site(url)
        urls = soup.find_all('a', class_='product-card-container')
        url_list = []
        for i in urls:
            url_list.append('https://minsu.meituan.com' + i["href"])
        return url_list

    def get_elements(self,url):
        r = requests.get(url,headers=self.headers)
        print(r.url)
        productId = r.url[-8:-1]
        comment_url = self.comment_url.format(productId)
        re = requests.get(comment_url, headers=self.headers)

        if r.status_code == 200:
            data = r.content.decode('utf-8')
            soup = BeautifulSoup(data,'lxml')
            dic = {}

            #获取评论
            comment_json = re.content.decode()
            comment_data = json.loads(comment_json)
            data_list = comment_data['data']['list']
            comment = ''
            for data_i in data_list:
                if data_i.get('body'):
                    comment += str(data_i['commentId']) + data_i['body'] + ';'
                else:
                    pass
                continue
            dic['comment'] = comment

            # 获取位置
            location = soup.select('#J-locationModule')[0].text.split('--')[1]
            loc_str = json.loads(location)

            # 产品ID ProductID
            dic['ProductID'] = productId
            # title 标题
            dic['title'] = soup.find('div', class_='text-clamp pointer').text
            # address 地址 latitiude 维度 longitiude纬度
            dic['address'] = loc_str['fullAddress']
            dic['lat'] = loc_str['lat']
            dic['lng'] = loc_str['lng']
            dic['loc_source'] = '腾讯地图'
            # 房屋价格/晚
            dic['price'] = soup.select('span[itemprop="price"]')[0].text
            # 房屋类型
            dic['style'] = soup.select('.specification__list')[0].text
            # print(dic['style'])
            # host 房东
            dic['host'] = soup.find('a', class_='nick-name S--host-link').text.replace(' ', '').strip('\n')
            # description 房东描述
            dic['description'] = soup.find('ul', class_='host-house-description').text.strip('\n')
            # link 网址链接
            dic['link'] = r.url
            dic['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            return dic
        else:
            return None

    def pandas_to_xlsx(self,data_info):
        pd_data = pd.DataFrame(data_info)
        pd_data.to_excel('美团民宿.xlsx',sheet_name='美团民宿')

    def save_to_mysql(self,dict_):
        t = ['ProductID','title','address','lat','lng','loc_source','price','style','host','description','link','datetime','comment']
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345', db='观前公安',
                                   charset="utf8")
            cursor = conn.cursor()
            insert_sql = """
                        insert into mtms(
                        ProductID,title,address,lat,lng,loc_source,price,style,host,description,link,datetime,comment
                        )
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            params = (dict_[t[0]], dict_[t[1]], dict_[t[2]], dict_[t[3]], dict_[t[4]], dict_[t[5]], dict_[t[6]], dict_[t[7]],
                dict_[t[8]], dict_[t[9]], dict_[t[10]], dict_[t[11]], dict_[t[12]])

            cursor.execute(insert_sql,params)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print('wrong:' + e)

    # 去重
    def is_exist(self,id_):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345', db='观前公安',
                               charset="utf8")
        cursor = conn.cursor()
        is_exist = cursor.execute("select * from mtms where ProductID = %s",(id_))  # 判断是否已存在该记录
        cursor.close()
        conn.close()
        return is_exist

    def main(self):
        page_list = self.get_page_list()
        urllist = []
        datas = []
        # 获取所有页面详情页链接
        for p in page_list:
            url_list = self.get_url_list(p)
            urllist.extend(url_list)  # 添加元素
        print('共找到%i个网址:' % len(urllist))

        # 详情页循环获取元素
        for url_i in urllist:
            # print(url_i)
            if self.is_exist(url_i[-8:-1]) != 0:
                try:
                    dic = self.get_elements(url_i)
                    time.sleep(1)
                    # 保存到数据库
                    self.save_to_mysql(dic)
                    datas.append(dic)   #添加字典
                    print('成功采集%i:' % len(datas))
                except Exception as e:
                    print(e)
            else:
                continue
        #保存到表格
        self.pandas_to_xlsx(datas)

if __name__ == '__main__':
    Meituan = Crawler()
    Meituan.main()