#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:mirco
# datetime:2019/8/6 17:25
# software: PyCharm

#上海垃圾分类

#方法一：随意打开一个B站视频，按F12，点开network按键，在左上方的输入区输入 list 便可找到相应的弹幕数据包。

#方法二：http://comment.bilibili.com/cid.xml  {99768393}

'''
API接口：
http://comment.bilibili.com/72036817.xml
https://api.bilibili.com/x/v1/dm/list.so?oid=9931722
数字是av号
但不是全部弹幕，只有一千条
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import jieba
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np

#请求弹幕数据
url = 'http://comment.bilibili.com/99768393.xml'
html = requests.get(url).content

#解析弹幕数据
html_data = str(html,'utf-8')
soup = BeautifulSoup(html_data,'lxml')
results = soup.find_all('d')

comments = [comment.text for comment in results]
comments_dict = {'comment':comments}

#将弹幕数据保存在本地
df = pd.DataFrame(comments_dict)
df.to_csv('blibili.csv',encoding='utf-8')

# 解析背景图片
mask_img = plt.imread('test.jpg')           #背景大小
mask_img2 = np.array(Image.open('2.png'))   #用来设定和限制形状

#设置词云样式
wc = WordCloud(
    # 设置字体
    font_path='SIMYOU.TTF',
    # 允许最大词汇量
    max_words=2000,
    # 设置最大号字体大小
    max_font_size=80,
    # 设置使用的背景图片
    mask=mask_img2,
    # 设置输出的图片背景色
    background_color=None, mode="RGBA",
    # 设置有多少种随机生成状态，即有多少种配色方案
    random_state=30)

# 读取文件内容
br = pd.read_csv('blibili.csv', header=None)

# 进行分词，并用空格连起来
text = ''
for line in br[1]:
    text += ' '.join(jieba.cut(line, cut_all=False))

wc.generate(text)
plt.imshow(wc)
plt.axis('off')     # 关闭坐标轴
plt.show()
