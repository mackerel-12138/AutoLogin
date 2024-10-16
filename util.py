import numpy as np
import os, sys, time, requests, pickle, re, random
from datetime import datetime
from retrying import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--headless') # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
proxy = os.getenv("proxy")
chrome_options.add_argument(f'--proxy-server={proxy}')  # 添加代理设置
user_agent = os.getenv("ua")
chrome_options.add_argument(f'user-agent={user_agent}')

def get_web_driver():
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

# 加载 Cookies
def load_cookies(driver, domain, cookiefile):
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['domain'] == domain:
            driver.delete_cookie(cookie['name'])
            print(f"删除 cookie: {cookie['name']}")

    if os.path.exists(cookiefile):
        with open(cookiefile, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("cookie加载成功")