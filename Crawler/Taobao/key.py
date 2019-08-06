# coding: utf-8

"""
Created on Sun Jan 14 12:20:33 2018

@author: Mirco
"""  

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)

def search():
    try:
        driver.get('https://www.taobao.com')
        #页面加载时间
        elements_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        #定位查询按钮  
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
        #提交关键词
        elements_input.send_keys('levis')
        submit.click() 
        getresult()
    except:
        return search()
    
    
def get_page():
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))
    result = int(re.findall(r'(\d+)',total.text)[0])
    return result
     
def next_page(page_num):
    input2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))) 
    input2.clear()
    input2.send_keys(page_num)
    submit.click()
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_num)))
    print (getresult())
    
def getresult():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items.item').items()
    for item in items:
        product = {
                'images': item.find('.img .jpg').attr('src'),  #class选择器
                'price': item.find('.price').text()[:-3],
                'deal': item.find('.deal-cnt').text()
                }
        print (product)
def main():
    search()
    total = get_page()
    print (total)
    for i in range(2,total + 1):
        next_page(i)

if __name__ == '__main__':
    main()