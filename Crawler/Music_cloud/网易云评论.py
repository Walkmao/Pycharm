# coding:utf-8
# __auth__ = "mirco"
# __date__ = "2020/11/2"

import base64
import codecs
import math
import os
import random
from Cryptodome.Cipher import AES
import requests
import time

# pip install pycryptodomex

# 参数加密类
class GetArgs(object):

    def __init__(self, dict):
        self.a_16 = self.a(16)
        self.dict = dict

    
    # 对应a函数
    def a(slef, a):
        b="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        c=""
        for i in range(a):
            e = random.random()*len(b)
            e = math.floor(e)
            c += b[e]
        return c


    # 转成16位数
    def to_16(self,key):
        while len(key) % 16 != 0:
            key += '\0'
        return key.encode('utf-8')
    
    # 对应的是js中的b函数
    # 具体语法请参照AES算法
    def AES_encrypt(self, text, key, iv):                                      # text为密文，key为公钥，iv为偏移量
        pad2 = lambda data: data + (16 - len(data.encode('utf-8')) % 16) * chr(16 - len(data.encode('utf-8')) % 16)
        # 此处为一坑,需要现将data转换为byte再来做填充，否则中文特殊字符等会报错
        data = pad2(text)
        encryptor = AES.new(self.to_16(key), AES.MODE_CBC, self.to_16(iv))
        encrypt_aes = encryptor.encrypt(data.encode('utf-8'))
        encrypt_text = base64.encodebytes(encrypt_aes)
        enctext = encrypt_text.decode('utf-8')
        return enctext

    
    # 获取params的值 
    def get_params(self):                         # song为歌曲名/返回值为params
        iv = "0102030405060708"
        g = '0CoJUm6Qyw8W8jud'
        i = self.a_16
        encText = str(self.dict)                # i8a
        return self.AES_encrypt(self.AES_encrypt(encText, g, iv), i, iv)

    # 对应js函数中的c函数
    # 具体语法请参照AES算法
    def RSA_encrypt(self,text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)
    
    # 获取encSecKey的值
    def get_encSecKey(self):
        i = self.a_16
        b = "010001"
        c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        return self.RSA_encrypt(i, b, c)


# 音乐下载类
class Music(object):

    def __init__(self):
        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        }
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://music.163.com/search/',
            'Connection': 'keep-alive',
            'cookie': '_iuqxldmzr_=32; _ntes_nnid=2c2050b762a20bec42d44b4ec9570db2,1596545803404; _ntes_nuid=2c2050b762a20bec42d44b4ec9570db2; WM_TID=P%2B9S%2BGxp32pBVAVRRQZqCt7Cgd%2BGver%2B; NMTID=00OeaJw_6w3Xsbamkk4mtz6A4aQ648AAAF0w8UCbA; WM_NI=uJgfo1tpOzmOzCi1zZbOYbXBDNPDlNewZXU3yQ3iumqfEggri%2BRhKdTEiIHOU2SXI3IuFjOG%2FKSi%2FAeBDlsY02AdcF3eDGC7oT5jbtTM7WD72FNddwZuZ8YelJFmI76NRXY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb6f0659a86fca5cc6093928fa6d14e968e9eaeb547898f8190d24686b7a0a7cb2af0fea7c3b92ab796a987ee3bb8b0819bf045ba9da7d2f952a2919783db4a8892a0a5ef46a7a996b9d839bb8ffd8af867b3ba8b88e67aabf59e89ca70989ba7aacb4597ee9db9cc398bab8a8bce4ded959d8aae4ba79e8c8df253f4ee8f85e24ef1bb8ca8c23dad8cfb8be1809893f9b8c73df29a8285e77d9aab96d9dc6fb0968a8ecc3df6929eb9dc37e2a3; JSESSIONID-WYYY=C1rSDXpSvPOpS%2FNHFyKe%5Cw3yY4%2F5bq5ntcfQ2QEqxSCJxkrD1%5CYeJdAGWIQmJpUIY5%5CtjA3S%2FrCedOHlKjFkPy5X4Eje7wt%2BHzgrcVRV%2BmXMRO8G%5CsxeUd9MBwwvqzIuEbuJkpv9mv6bCvQBzI9bI1qQl8WnFzFvy5Z0SqVeIAGYexqB%3A1601034012504'
        }  # 请求头
        self.url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        s = input('请输入想要听的歌：')
        self.arg = {'csrf_token': "", 'hlposttag': '<span class="s-fc\">', 'limit': '30', 'offset': '0', 's': '{0}'.format(s), 'total': 'true', 'type': '1'}
        self.class_arg = GetArgs(self.arg)
        self.params = {
            'params': self.class_arg.get_params(),
            'encSecKey': self.class_arg.get_encSecKey()
        }
        self.song = []
        self.singer = []
        self.id = []
        self.dt = []

    # 搜索音乐
    def search(self):
        response = requests.post(self.url, headers=self.headers, data=self.params)
        dict = response.json()
        music_list = dict['result']['songs']
        # print(music_list)
        for music in music_list:
            self.song.append(music['name'])
            self.singer.append(music['ar'][0]['name'])
            self.id.append(music['id'])
            self.dt.append(music['dt'])
        self.select()

    # 选中那首音乐
    def select(self):
        ip = 0
        for song, singer, id, dt in zip(self.song, self.singer, self.id, self.dt):
            min = int(int(dt) / 1000 / 60)
            seconds = int(int(dt) / 1000 % 60)
            time = str(min)+":"+str(seconds)
            print(ip, song, singer, time)
            ip += 1
        ip = input("请输入序号：")
        ip = int(ip)
        song = self.song[ip]
        singer = self.singer[ip]
        id = self.id[ip]
        print(song, singer, id)
        choise_act = input("想要下载音乐还是评论：1音乐  2评论")
        select_num = int(choise_act)
        if select_num == 1:
            self.download(song, singer, id)
        else:
            self.comment_spider(id)

    # 音乐下载方法
    def download(self, song, singer, id):
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        arg = {
            'csrf_token': '',
            'encodeType': 'aac',
            'ids': "[" + '{0}'.format(id) + "]",
            'level': 'standard'
        }
        class_arg = GetArgs(arg)
        params = {
            'params': class_arg.get_params(),
            'encSecKey': class_arg.get_encSecKey()
        }
        response = requests.post(url, headers=self.headers, data=params)
        dict = response.json()
        url = dict['data'][0]['url']
        music = requests.get(url, headers=self.headers2).content
        dir = os.getcwd()
        dir = os.path.join(dir, "网易云音乐 ")
        if not os.path.exists(dir):
            os.mkdir(dir)  # 构造文件夹
        os.chdir(dir)  # 将下载的歌曲存储在该文件夹
        print(song, singer)
        file_name = song + '-' + singer + '.m4a'  # 文件名
        with open(file_name, 'wb') as f:
            f.write(music)
        print("下载成功！")

    # 评论爬取方法
    def comment_spider(self, song_id):
        # post请求的url
        req_url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
        # 请求头
        cur_headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://music.163.com/song?id={}'.format(id),
            'Connection': 'keep-alive',
            'cookie': '_iuqxldmzr_=32; _ntes_nnid=2c2050b762a20bec42d44b4ec9570db2,1596545803404; _ntes_nuid=2c2050b762a20bec42d44b4ec9570db2; WM_TID=P%2B9S%2BGxp32pBVAVRRQZqCt7Cgd%2BGver%2B; NMTID=00OeaJw_6w3Xsbamkk4mtz6A4aQ648AAAF0w8UCbA; WM_NI=uJgfo1tpOzmOzCi1zZbOYbXBDNPDlNewZXU3yQ3iumqfEggri%2BRhKdTEiIHOU2SXI3IuFjOG%2FKSi%2FAeBDlsY02AdcF3eDGC7oT5jbtTM7WD72FNddwZuZ8YelJFmI76NRXY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb6f0659a86fca5cc6093928fa6d14e968e9eaeb547898f8190d24686b7a0a7cb2af0fea7c3b92ab796a987ee3bb8b0819bf045ba9da7d2f952a2919783db4a8892a0a5ef46a7a996b9d839bb8ffd8af867b3ba8b88e67aabf59e89ca70989ba7aacb4597ee9db9cc398bab8a8bce4ded959d8aae4ba79e8c8df253f4ee8f85e24ef1bb8ca8c23dad8cfb8be1809893f9b8c73df29a8285e77d9aab96d9dc6fb0968a8ecc3df6929eb9dc37e2a3; JSESSIONID-WYYY=C1rSDXpSvPOpS%2FNHFyKe%5Cw3yY4%2F5bq5ntcfQ2QEqxSCJxkrD1%5CYeJdAGWIQmJpUIY5%5CtjA3S%2FrCedOHlKjFkPy5X4Eje7wt%2BHzgrcVRV%2BmXMRO8G%5CsxeUd9MBwwvqzIuEbuJkpv9mv6bCvQBzI9bI1qQl8WnFzFvy5Z0SqVeIAGYexqB%3A1601034012504'
        }
        # 构建参数请求第一页评论  获取评论总数
        response = self.send_req(req_url, 1, cur_headers, song_id)
        # 将json格式字符串转换成python字典，
        com_dict = response.json()
        total_comment = int(com_dict['data']['totalCount'])
        total_page = total_comment/20
        if total_comment % 20 != 0:
            # 获取总页数
            total_page = total_page+1
            comment_data = self.music_comments(total_page, req_url, cur_headers, song_id)
            print('数据采集完毕，正在往本地写入!')
        else:
            # 获取总页数
            comment_data = self.music_comments(total_page, req_url, cur_headers, song_id)
            print('数据采集完毕，正在往本地写入!')

        print(comment_data)
        self.write_file(comment_data)

    # 处理每页评论 爬取每页数据
    def music_comments(self, total_page, req_url, cur_headers, song_id):
        commentinfo = []
        # 对每一页评论
        for cur_page in range(1, int(total_page + 1)):
                r = self.send_req(req_url, cur_page,  cur_headers, song_id)
                # print(r.json())
                try:
                    comment_info = r.json()['data']['comments']
                    for i in comment_info:
                        com_info = {}
                        com_info['content'] = i['content']
                        com_info['author'] = i['user']['nickname']
                        com_info['likedCount'] = i['likedCount']
                        # print(com_info)
                        commentinfo.append(com_info)
                        # print("--"*50)
                    print("正在爬取第{}页".format(cur_page))
                    # time.sleep(10)
                except(KeyError):
                    return commentinfo


    # 构建评论参数 发送请求
    def send_req(self, req_url, page, cur_headers, id):
        # post的参数
        arg = {
            'csrf_token': "",
            'offset': str((page-1)*20),
            'pageNo': "{}".format(page),          # 第几页
            'pageSize': "20",                     # 页数
            'rid': "R_SO_4_{}".format(id),            # 和歌曲id拼接的参数
            'threadId': "R_SO_4_{}".format(id),        # 和歌曲id拼接的参数
            'orderType': "1"
        }
        print(arg)
        class_arg = GetArgs(arg)
        params = {
            'params': class_arg.get_params(),
            'encSecKey': class_arg.get_encSecKey()
        }
        # print(params)
        response = requests.post(req_url, headers=cur_headers, data=params)
        return response

       #写入数据
    def write_file(self, comment_data):
        with open("网易云评论.txt","a",encoding='UTF-8') as f:
            for content in comment_data:
                f.write(content['author']+" 说： "+content['content'])
                f.write("\n\n")


if __name__ == '__main__':
    music = Music()
    music.search()

