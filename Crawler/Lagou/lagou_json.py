import requests
import json
import time
import pandas as pd
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'referer': 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
}

def parse_position_list():
    url_start = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
    url_parse = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    data = {
        'first': 'false',
        'pn': 1,
        'kd': 'python'
    }
    s = requests.Session() # 创建一个session对象
    s.get(url_start, headers=headers, timeout=3)  # 用session对象发出get请求，请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies

    # 循环多页爬取
    datas = []

    for i in range(1,2):
        data['pn'] = i
        response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        result = json.loads(response.content.decode('utf-8'))
        # print(result)
        positions = result['content']['positionResult']['result']

        for position in positions:
            dicc = {}
            dicc['positionId'] = position['positionId']
            dicc['positionName'] = position['positionName']
            dicc['companyFullName'] = position['companyFullName']
            dicc['city'] = position['city']
            dicc['district'] = position['district']
            dicc['salary'] = position['salary']
            dicc['workYear'] = position['workYear']
            dicc['jobNature'] = position['jobNature']
            dicc['education'] = position['education']
            dicc['latitude'] = position['latitude']
            dicc['longitude'] = position['longitude']

            # 下面获取详情页信息
            parse_url = 'https://www.lagou.com/jobs/{}.html'.format(dicc['positionId'])
            dicc['description'] = parse_position_detail(parse_url)
            datas.append(dicc)
        time.sleep(2)
    return datas

def parse_position_detail(url):
    responses = requests.get(url, headers=headers)
    html = etree.HTML(responses.content.decode())
    description = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
    return description

def save_datas(datas):
    pd_datas = pd.DataFrame(datas)
    print(pd_datas)
    pd_datas.to_csv('lagou.csv',encoding='utf-8')

def main():
    datas = parse_position_list()
    save_datas(datas)

if __name__ == '__main__':
    main()