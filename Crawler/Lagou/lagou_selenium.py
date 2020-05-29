# 显示等待 + 窗口切换

import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


# 获取详情页的所有职位的链接地址url
def parse_list_page():
    # 获取详情页url
    links = driver.find_elements_by_xpath("//a[@class='position_link']")
    link_list = [link.get_attribute('href') for link in links]  # 把所有url放到list列表中
    return link_list


# 获取详情页的职位信息
def parse_position_detail(url):
    driver.execute_script("window.open('%s')" % url)
    driver.switch_to.window(driver.window_handles[1])

    wait.until(
        EC.presence_of_element_located((By.ID, "job_detail"))
    )
    job_detail = driver.find_element_by_id('job_detail').text
    print(job_detail)


# 循环获取每一页中职位列表详情信息
def request_position():
    # 获取当前页中职位列表的url
    link_list = parse_list_page()

    for link in link_list[:1]:   # 这里仅供测试，打印一页中前两个职位详情
        parse_position_detail(link)

        # print(driver.current_window_handle)  # 打印当前的窗口话柄
        driver.close()        # 关闭详情页
        driver.switch_to.window(driver.window_handles[0])  # 切换到首页
        time.sleep(1)

def main():
    url_start = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
    driver.get(url_start)

    # 打开网站出现其他嵌入式的广告，需要取消
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "body-btn")))
    driver.find_element_by_class_name("body-btn").click()

    page_num = 1
    while True:
        try:
            # 1.等待下一页按钮加载完成
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "pager_next"))
            )

            # 2.获取当前页职位列表中的详情信息
            print('****正在打印第{}页****'.format(page_num))
            request_position()

            # 3.点击获取下一页按钮
            next_box = driver.find_element_by_class_name("pager_next")
            next_box.click()
            page_num += 1

        except:
            driver.quit()

if __name__ == '__main__':
    main()