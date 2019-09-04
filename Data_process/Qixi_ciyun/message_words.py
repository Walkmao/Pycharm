#!/usr/bin/env python3
# coding: utf-8
# author:mirco
# datetime:2019/8/6 11:12
# software: PyCharm

import jieba
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 剔除大量的标点符号，包括日期，表情等等，这里选择直接匹配中文
pattern  = re.compile(u"[\u4e00-\u9fa5]+")
#“\u4e00”和“\u9fa5”是unicode编码，并且正好是中文编码的开始和结束的两个值,至少匹配一个汉字。

with open('words.txt','r',encoding='gbk') as f:       #encoding='utf-8'报错
    data = re.findall(pattern,f.read())
    data = ''.join(data)
print(data)

with open('clear.txt','w') as f:    #如果没有文件将自动生成
    f.write(data)

def word_cloud(data_path, mask_path):
    with open(data_path,'r') as f:
        data = f.read()

    mask = plt.imread(mask_path)    #解析背景图片
    cut_data = jieba.cut(data)
    str_cut_data = ' '.join(cut_data)
    list_cut_data = str_cut_data.split(' ')

    my_wordcloud = WordCloud(font_path = './simfang.ttf',mask=mask,background_color='pink').generate(str_cut_data)

    plt.imshow(my_wordcloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    word_cloud('clear.txt',r'C:\Users\mirco\Desktop\1.jpg')