# 0、导入模块
from bs4 import BeautifulSoup
import requests
import random
import time
from multiprocessing import Pool
import csv
import pymongo

# 0、创建数据库
client = pymongo.MongoClient('localhost', 27017)
Amazon = client['Amazon']
reviews_info_M = Amazon['reviews_info_M']

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


# 1、读取csv中的'Rank','item_name','reviews','reviews_link'
csv_file = csv.reader(open('C:/Users/zbd/Desktop/3.csv','r'))
reviews_datalst = []
for i in csv_file:
    reviews_data = {
        'Rank':i[10],
        'item_name':i[8],
        'reviews':i[6],
        'reviews_link':i[5]
    }
    reviews_datalst.append(reviews_data)
del reviews_datalst[0]    # 删除表头
#print(reviews_datalst)
reviews_links = list(i['reviews_link'] for i in reviews_datalst)  # 将评论详情页链接存储到列表reviews_links

# 清洗reviews,其中有空值或者“1,234”样式
reviews = []
for i in reviews_datalst:
    if i['reviews']:
        reviews.append(int(i['reviews'].replace(',','')))
    else:
        reviews.append(0)
print(reviews_links)
print(reviews)

# 2、抓取每个商品的评论页链接
# 商品 1
# 第1页：https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
# 第2页：https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2
# 第3页：https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3
# 商品 2
# 第1页：https://www.amazon.com/Avidlove-Women-Lingerie-Babydoll-Bodysuit/product-reviews/B077CLFWVN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
# 第2页：https://www.amazon.com/Avidlove-Women-Lingerie-Babydoll-Bodysuit/product-reviews/B077CLFWVN/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2
# 每页有8个评论，pages = reviews // 8 + 1
# 目标格式：https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/pageNumber=1
url = 'https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
counts = 0
def get_item_reviews(reviews_link,reviews):
    if reviews_link:
        pages = reviews // 8  # 每页有8个评论，pages = reviews // 8 ,最后一页不爬取
        for i in range(1,pages+1):
            full_url = reviews_link.split('ref=')[0] + '?pageNumber={}'.format(i)
            #full_url = 'https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/?pageNumber=10'
            wb_data = requests.get(full_url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            every_page_reviews_num = len(soup.select('div.a-row.a-spacing-small.review-data > span'))
            for j in range(every_page_reviews_num):
                reviews_info ={
                    'customer_name' : soup.select('div:nth-child(1) > a > div.a-profile-content > span')[j].text,
                    'star'          : soup.select('div.a-row>a.a-link-normal > i > span')[j].text.split('out')[0],
                    'review_date'   : soup.select('div.a-section.review >div>div>  span.a-size-base.a-color-secondary.review-date')[j].text,
                    'review_title'  : soup.select('a.a-size-base.a-link-normal.review-title.a-color-base.a-text-bold')[j].text,
                    'review_text'   : soup.select('div.a-row.a-spacing-small.review-data > span')[j].text,
                    'item_name'     : soup.title.text.split(':')[-1]
                }
                yield reviews_info
                reviews_info_M.insert_one(reviews_info)
                global  counts
                counts +=1
                print('第{}条评论'.format(counts),reviews_info)
    else:
        pass

'''
# 这边主要是爬取size和color，因为其数据大量缺失，所以另外爬取
# 与上一步的代码基本一样，主要在于要确认每页评论的size&color个数
# 写入数据库和csv也需要作相应修改，但方法相同

def get_item_reviews(reviews_link,reviews):
    if reviews_link:
        pages = reviews // 8  # 每页有8个评论，pages = reviews // 8 ,最后一页不爬取，要做一个小于8个评论的判断
        for i in range(1,pages+1):
            full_url = reviews_link.split('ref=')[0] + '?pageNumber={}'.format(i)
            #full_url = 'https://www.amazon.com/Avidlove-Lingerie-Babydoll-Sleepwear-Chemise/product-reviews/B0712188H2/?pageNumber=10'
            wb_data = requests.get(full_url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            every_page_reviews_num = len(soup.select('div.a-row.a-spacing-mini.review-data.review-format-strip > a'))   # 每页的size&color个数
            for j in range(every_page_reviews_num):
                reviews_info ={
                    'item_name'     : soup.title.text.split(':')[-1],
                    'size_color'    : soup.select('div.a-row.a-spacing-mini.review-data.review-format-strip > a')[j].text,
                }
                yield reviews_info
                print(reviews_info)
                reviews_size_color.insert_one(reviews_info)
        else:
            pass
'''


# 3、开始爬取和存储数据
all_reviews = []
def get_all_reviews(reviews_links,reviews):
    for i in range(100):
        for n in get_item_reviews(reviews_links[i],reviews[i]):
            all_reviews.append(n)

get_all_reviews(reviews_links,reviews)
#print(all_reviews)


# 4、写入csv
headers = ['_id','item_name', 'customer_name', 'star', 'review_date', 'review_title', 'review_text']
with open('C:/Users/zbd/Desktop/4.csv','w',newline='',encoding='utf-8') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(all_reviews)
print('写入完毕！')

















