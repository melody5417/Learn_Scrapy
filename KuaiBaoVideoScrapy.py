# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from browsermobproxy import Server

# init proxy
server = Server("/Users/yiqiwang/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()
# proxy.whitelist("http://ugcws.video.gtimg.com/*", 200)

# init chrome
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host = "localhost", port = proxy.port))
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(10)


proxy.new_har("kuaibao_monitor",options={'captureHeaders':True})

# 打开网页
driver.get("http://kuaibao.qq.com/s/20190107V14QLN00")


# 查找播放按钮 并 点击
driver.find_element_by_css_selector("use.txp_svg_symbol.txp_svg_play").click()

# 提取 url
video_url = ""
while len(video_url) == 0:
    result = proxy.har
    for entry in result['log']['entries']:
        _url = entry['request']['url']

        if _url.startswith('http://ugcws.video.gtimg.com/'):
            video_url = _url
            break

print(video_url)



# server.stop()
# driver.quit()
