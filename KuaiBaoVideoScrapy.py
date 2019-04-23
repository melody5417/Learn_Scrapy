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

# define

PathToBrowsermobProxy = "/Users/yiqiwang/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"

# init proxy
server = Server(path=PathToBrowsermobProxy)
server.start()
proxy = server.create_proxy()

# init chrome
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-agent={user_agent}'.format(user_agent=USER_AGENT))
chrome_options.add_argument('--proxy-server={host}:{port}'.format(host="localhost", port=proxy.port))
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(10)

# open page
driver.get("http://kuaibao.qq.com/s/20190107V14QLN00")

# init har
proxy.new_har("kuaibao_monitor",options={'captureHeaders':True, 'captureContent':True})

# find element and click
driver.find_element_by_css_selector("use.txp_svg_symbol.txp_svg_play").click()

# fetch url
video_url = ""
while len(video_url) == 0:
    result = proxy.har

    # dict_keys(['pageref', 'startedDateTime', 'request', 'response', 'cache', 'timings', 'serverIPAddress', 'comment', 'time'])
    # dic = result['log']['entries'][0]
    # print(dic.keys())

    for entry in result['log']['entries']:
        _url = entry['request']['url']
        _rsp = entry['response']
        _headers = _rsp['headers']

        # {'status': 200, 'statusText': 'OK', 'httpVersion': 'HTTP/1.1', 'cookies': [],
        #  'headers': [{'name': 'Date', 'value': 'Tue, 23 Apr 2019 03:35:29 GMT'},
        #              {'name': 'Content-Type', 'value': 'application/xml; charset=utf-8'},
        #              {'name': 'Transfer-Encoding', 'value': 'chunked'}, {'name': 'Connection', 'value': 'keep-alive'},
        #              {'name': 'Server', 'value': 'openresty'}, {'name': 'X-Powered-By', 'value': 'HHVM/3.7.3-dev'},
        #              {'name': 'X-Location', 'value': '/'}, {'name': 'X-Client-Ip', 'value': '61.135.172.68'},
        #              {'name': 'X-Server-Ip', 'value': '125.39.133.120'}],
        #  'content': {'size': 0, 'mimeType': 'application/xml; charset=utf-8', 'text': '', 'comment': ''},
        #  'redirectURL': '', 'headersSize': 277, 'bodySize': 0, 'comment': ''}

        # check if content-type is "application/octet-stream"
        for _header in _headers:
            if _header['name'] == 'Content-Type':
                if _header['value'] == 'application/octet-stream':
                    video_url = _url
                    break

print(video_url)