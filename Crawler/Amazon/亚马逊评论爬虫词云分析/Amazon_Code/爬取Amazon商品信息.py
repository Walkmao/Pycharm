# 0、导入模块
from bs4 import BeautifulSoup
import requests
import random
import time
from multiprocessing import Pool
import pymongo

# 0、创建数据库
client = pymongo.MongoClient('localhost', 27017)
Amazon = client['Amazon']
item_info_M = Amazon['item_info_M']

# 0、反爬措施
headers  = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
# http://cn-proxy.com/
proxy_list = [
    'http://117.177.250.151:8081',
    'http://111.85.219.250:3129',
    'http://122.70.183.138:8118',
    ]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies = {'http': proxy_ip}

# 1、爬取商品排名和详情页链接
url_page1 = 'https://www.amazon.com/Best-Sellers-Womens-Chemises-Negligees/zgbs/fashion/1044968/ref=zg_bs_pg_1?_encoding=UTF8&pg=1'  # 01-50名商品
url_page2 = 'https://www.amazon.com/Best-Sellers-Womens-Chemises-Negligees/zgbs/fashion/1044968/ref=zg_bs_pg_2?_encoding=UTF8&pg=2'  # 51-100名商品

item_info = []    # 存储商品详细信息的列表
item_links = []   # 存储商品详情页链接的列表
def get_item_info(url):
    wb_data = requests.get(url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for i in range(50):
        data = {
            'Rank': soup.select('span.zg-badge-text')[i].text.strip('#'),
            'item_name' : soup.select('#zg-ordered-list > li > span > div > span > a > div')[i].text.strip(),
            'item_link' : 'https://www.amazon.com' + soup.select('#zg-ordered-list > li > span > div > span > a')[i].get('href'),
            'img_src' :soup.select('#zg-ordered-list > li> span > div > span > a > span > div > img')[i].get('src')
        }
        item_info.append(data)
        item_links.append(data['item_link'])
    print('finish!')

get_item_info(url_page1)
get_item_info(url_page2)


# 2、在商品详情页爬取更多商品信息
#item_url = 'https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/dp/B0712188H2/ref=zg_bs_1044968_1?_encoding=UTF8&refRID=MYWGH1W2P3HNS58R4WES'
def get_item_info_2(item_url,data):
    wb_data = requests.get(item_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    #获取price（需要判断）
    price = soup.select('#priceblock_ourprice')
    data['price'] = price[0].text if price else None

    # 获取star和reviews（需要判断）
    star = soup.select('div>div>span>span>span>a>i>span.a-icon-alt')
    if star:
        data['star'] = star[0].text.split(' ')[0]
        data['reviews'] = soup.select('#reviews-medley-footer > div.a-row.a-spacing-large > a')[0].text.split(' ')[2]
        data['Read reviews that mention'] = list(i.text.strip('\n').strip() for i in soup.select('span.cr-lighthouse-term'))
    else:
        data['star'] = None
        data['reviews'] = None
        data['Read reviews that mention'] = None

    data['Date_first_listed_on_Amazon'] = soup.select('#detailBullets_feature_div > ul > li> span > span:nth-child(2)')[-1].text

    # 获取reviews_link（需要判断）
    reviews_link = soup.select('#reviews-medley-footer > div.a-row.a-spacing-large > a')
    if reviews_link:
        data['reviews_link'] = 'https://www.amazon.com' + reviews_link[0].get('href')
    else:
        data['reviews_link'] = None

    # 获取store和store_link （需要判断）
    store = soup.select('#bylineInfo')
    if store:
        data['store'] = store[0].text
        data['store_link'] = 'https://www.amazon.com' + soup.select('#bylineInfo')[0].get('href')
    else:
        data['store'] = None
        data['store_link'] = None

    item_info_M.insert_one(data)   # 存入MongoDB数据库
    print(data)


# 3、将商品详情写入csv文件
for i in range(100):
    get_item_info_2(item_links[i],item_info[i])
    print('已写入第{}个商品'.format(i+1))

import csv
headers = ['_id','store', 'price', 'Date_first_listed_on_Amazon', 'item_link', 'reviews_link', 'reviews', 'store_link', 'item_name', 'img_src', 'Rank', 'Read reviews that mention', 'star']
with open('C:/Users/Mirco/Desktop/3.csv','w',newline='',encoding='utf-8') as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(item_info)

print('写入完毕！')