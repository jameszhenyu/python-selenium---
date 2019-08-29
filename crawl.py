#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver

# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains
# 等待时间 产生随机数
import time
import random
import pandas as pd
import numpy as np
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait


def get_info():

    div_list = re.xpath('//*[@id="web-content"]/div/div[1]/div[2]/div[2]/div')
    profession=re.xpath('//*[@id="search-filter"]/div[2]/div[1]/div/a[3]/text()')
    location=re.xpath('//*[@id="search-filter"]/div[2]/div[1]/div/a[2]/text()')
    profession=profession[0][5:]
    location=location[0][3:]


    # //*[@id="web-content"]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[3]/div[1]/span[2]/span
    # //*[@id="web-content"]/div/div[1]/div[2]/div[2]/div[6]/div/div[3]/div[4]/div/span[2]/span
    name_store = []
    id_store = []
    time_store = []
    phone_store = []
    loc=[]#地点
    pro=[]#职业
    for i in div_list:
        name = i.xpath('div/div[3]/div[1]/a/text()')[0]
        id = i.xpath('div/div[3]/div[2]/div[1]/a/text()')
        if id == []:
            id = i.xpath('div/div[3]/div[3]/div[1]/a/text()')

        time = i.xpath('div/div[3]/div[2]/div[3]/span/text()')
        if time == []:
            time = i.xpath('div/div[3]/div[3]/div[3]/span/text()')
        phone = i.xpath('div/div[3]/div[3]/div[1]/span[2]/span/text()')
        if phone == []:
            phone = i.xpath('div/div[3]/div[4]/div/span[2]/span/text()')

        name_store.append(name)
        id_store.append(id)
        time_store.append(time)
        phone_store.append(phone)
        loc.append(location)
        pro.append(profession)

    data = pd.DataFrame({'公司名称': np.array(name_store).reshape(-1),
                         '法定代表': np.array(id_store).reshape(-1),
                         '成立时间': np.array(time_store).reshape(-1),
                         '电话号码': np.array(phone_store).reshape(-1),
                         '地点':np.array(loc),
                         '行业':np.array(pro)})
    print(data)

    Data_store.append(data)


if __name__ == '__main__':
    Data_store = []
    driver = webdriver.Chrome()
    driver.get("https://www.tianyancha.com/search?base=hangzhou")
    driver.maximize_window()
    # 点击登录链接
    # loginLink = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//a[@οnclick="header.loginLink(event)"]'))
    loginLink = driver.find_element_by_css_selector(
        '#web-content > div > div.container > div > div.login-right > div > div.module.module1.module2.loginmodule.collapse.in > div.title-tab.text-center > div.title.-active')
    print(loginLink.text)
    loginLink.click()

    # 切换到密码登录方式
    # login_by_pwd = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@οnclick="loginObj.changeCurrent(1);"]'))
    login_by_pwd = driver.find_element_by_xpath('//div[text()="密码登录"]')
    print(login_by_pwd.text)
    login_by_pwd.click()

    # 输入用户名
    username = driver.find_element_by_css_selector(
        '#web-content > div > div.container > div > div.login-right > div > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.f-base.collapse.in > div.pb30.position-rel > input')
    username.send_keys('你的用户名')

    # 输入密码
    password = driver.find_element_by_css_selector(
        'div.input-warp.-block > input.input.contactword')
    password.send_keys('你的密码')

    login_button = driver.find_element_by_xpath('//div[text()="登录"]')
    login_button.click()
    time.sleep(20)

    html = driver.page_source
    re = etree.HTML(html)
    page_num = re.xpath('//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[12]/a/text()')
    print(page_num)
    get_info()
    time.sleep(3)

    for link in driver.find_elements_by_xpath(
            '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[12]/a'):
        href = (link.get_attribute('href'))
        driver.get(href)
        html = driver.page_source
        re = etree.HTML(html)
        get_info()

    time.sleep(6)

    for i in range(4):
        for link in driver.find_elements_by_xpath(
                '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[13]/a'):
            href = (link.get_attribute('href'))
            driver.get(href)
            html = driver.page_source
            re = etree.HTML(html)
            get_info()
        print(i)
    print('前5页')

    for j in range(150):
        if j >10:
            time.sleep(4)




        for link in driver.find_elements_by_xpath(  # https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%2Foe01-s2-hp1%2Fp114%3Fbase%3Dhangzhou&rnd=
                '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[14]/a'):
            # url = driver.current_url
            # print(url)
            #url = 'https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%2Foe01-s2-hp1%2Fp102%3Fbase%3Dhangzhou&rnd='


            href = (link.get_attribute('href'))
            driver.get(href)


            html = driver.page_source
            re = etree.HTML(html)
            get_info()
        print(j)




    data = pd.concat(Data_store, ignore_index=True)
    data.to_csv('C:\\Users\\Administrator\\Desktop\\w\\data3.csv', index=False)
