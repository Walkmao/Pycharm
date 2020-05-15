#!/usr/bin/env python
# coding=utf-8
import sys
import time
import json
import xlsxwriter
from selenium import webdriver

url = "https://inn.ctrip.com/onlineinn/newdetail/15447055"

# 谷歌驱动
def chrome_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver

# 获取信息
def get_info(driver):
    item = {
        'info':driver.find_element_by_xpath('/html/body/script[1]').text
        # 'info':driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[1]').text,
        # 'type_of_house':driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[3]/div[4]/div[1]/div[2]/span[1]').text,
        # 'num_of_people':driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[3]/div[4]/div[1]/div[3]/span[1]').text,
        # 'num_of_bed':driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[3]/div[4]/div[1]/div[3]/span[2]').text,
        # 'locate':driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[3]/span').text,
        # 'url':driver.current_url,
        # 'price':driver.find_element_by_class_name('txt-price').text
    }
    return item

if __name__ == "__main__":
    driver = chrome_driver(url)
    data = get_info(driver)

