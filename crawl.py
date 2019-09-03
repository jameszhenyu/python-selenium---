#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from sqlalchemy import create_engine
from selenium.webdriver.common.keys import Keys
import pymysql
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
    
    Data_store = []
    div_list = re.xpath('//*[@id="web-content"]/div/div[1]/div[2]/div[2]/div')
    profession = re.xpath(
        '//*[@id="search-filter"]/div[2]/div[1]/div/a[3]/text()')
    location = re.xpath(
        '//*[@id="search-filter"]/div[2]/div[1]/div/a[2]/text()')
    profession = profession[0][5:]
    location = location[0][3:]

    # //*[@id="web-content"]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div[3]/div[1]/span[2]/span
    # //*[@id="web-content"]/div/div[1]/div[2]/div[2]/div[6]/div/div[3]/div[4]/div/span[2]/span
    name_store = []
    id_store = []
    time_store = []
    phone_store = []
    loc = []  # 地点
    pro = []  # 职业
    for i in div_list:
        name = i.xpath('div/div[3]/div[1]/a/text()')[0]
        id = i.xpath('div/div[3]/div[2]/div[1]/a/text()')
        if id == []:
            id = i.xpath('div/div[3]/div[3]/div[1]/a/text()')
        if id == []:
            id = 'none'

        if isinstance(id, list):
            id = id[0]

        time = i.xpath('div/div[3]/div[2]/div[3]/span/text()')
        if time == []:
            time = i.xpath('div/div[3]/div[3]/div[3]/span/text()')

        phone = i.xpath('div/div[3]/div[3]/div[1]/span[2]/span/text()')
        if phone == []:
            phone = i.xpath('div/div[3]/div[4]/div/span[2]/span/text()')
        if isinstance(phone, list):  # 判断数据类型是不是为str，如果字符类型为list，抽有用字段
            phone = phone[0]

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
                         '地点': np.array(loc),
                         '行业': np.array(pro)})
    print(data)

    Data_store.append(data)
    data = pd.concat(Data_store, ignore_index=True)
    data = data.drop_duplicates()
    write_into_mysql(data)


def write_into_mysql(data):

    # DataFrame 写入数据库
    conn = create_engine(
        'mysql+pymysql://root:123456@localhost:3306/mysql',
        encoding='utf8')
    # 写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    pd.io.sql.to_sql(data, "crawl_sub", conn, if_exists='append')


if __name__ == '__main__':
    
    driver = webdriver.Chrome()
    driver.get("https://www.tianyancha.com/search?base=hangzhou")
    driver.maximize_window()
    # 点击登录链接
    # loginLink = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//a[@οnclick="header.loginLink(event)"]'))
    loginLink = driver.find_element_by_css_selector(
        'body > div.tyc-header > div > div.right > div > div:nth-child(4) > a')
    print(loginLink.text)
    loginLink.click()

    # 切换到密码登录方式
    # login_by_pwd = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@οnclick="loginObj.changeCurrent(1);"]'))
    login_by_pwd = driver.find_element_by_xpath('//div[text()="密码登录"]')
    print(login_by_pwd.text)
    login_by_pwd.click()

    # 输入用户名

    username = driver.find_elements_by_css_selector(
        "div.pb30.position-rel > input")[2]  # webelement 有四个只有一个可见
    username.send_keys("13857102700")

    # 输入密码
    password = driver.find_element_by_css_selector(
        'div.input-warp.-block > input')
    password.send_keys('abcde12345')

    login_button = driver.find_element_by_xpath('//div[text()="登录"]')
    login_button.click()
    time.sleep(20)

    html = driver.page_source
    re = etree.HTML(html)


    page_num = re.xpath(
            '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[11]/a/text()')[0].strip('.')




    page_num = int(page_num)

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

    for j in range(4, page_num - 7):
        if j > 10:
            time.sleep(4)

        for link in driver.find_elements_by_xpath(  # https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%2Foe01-s2-hp1%2Fp114%3Fbase%3Dhangzhou&rnd=
                '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[14]/a'):

            href = (link.get_attribute('href'))
            driver.get(href)
            html = driver.page_source
            re = etree.HTML(html)
            get_info()
        print(j)

    for k in range(page_num - 7, page_num - 2):
        if k > 10:
            time.sleep(4)

        for link in driver.find_elements_by_xpath(
                # https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%2Foe01-s2-hp1%2Fp114%3Fbase%3Dhangzhou&rnd=
                '//*[@id="web-content"]/div/div[1]/div[2]/div[3]/div/ul/li[13]/a'):
            href = (link.get_attribute('href'))
            driver.get(href)
            html = driver.page_source
            re = etree.HTML(html)
            get_info()
        print(k)
