# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from browsermobproxy import Server
import pandas as pd
import time

# define
PathToExcelFile = "/Users/yiqiwang/Desktop/video_list.xlsx"
Column_Name = "文章链接"
PathToBrowsermobProxy = "/Users/yiqiwang/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy"
User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"


def initProxy(path):
    server = Server(path=path)
    server.start()
    proxy = server.create_proxy()
    proxy.new_har("kuaibao_monitor", options={'captureHeaders': True, 'captureContent': True})
    return proxy

def initDriver(port):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--user-agent={user_agent}'.format(user_agent=User_Agent))
    chrome_options.add_argument('--proxy-server={host}:{port}'.format(host="localhost", port=port))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def readFile(path):
    data_frame = pd.read_excel(PathToExcelFile)
    return data_frame[Column_Name]

def getPage(proxy, driver, h5Url):
    # open page
    print("start scrapying " + h5Url)
    driver.get(h5Url)

    # find element and click
    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "use.txp_svg_symbol.txp_svg_play"))
        )
    except:
        print("error: " + url)
        return

    driver.find_element_by_css_selector("use.txp_svg_symbol.txp_svg_play").click()

    # fetch url
    video_url = ""
    while len(video_url) == 0:
        result = proxy.har

        # dict_keys(['pageref', 'startedDateTime', 'request', 'response', 'cache', 'timings', 'serverIPAddress', 'comment', 'time'])
        for entry in result['log']['entries']:
            if len(video_url) != 0:
                break

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
                        if ("mp4" in _url) or ("ugc" in _url):
                            video_url = _url
                            break

    print(video_url)

if __name__ == '__main__':
    proxy = initProxy(path=PathToBrowsermobProxy)
    driver = initDriver(proxy.port)
    h5Urls = readFile(path=PathToExcelFile)
    for url in h5Urls[10:21]:
        getPage(proxy=proxy, driver=driver, h5Url=url)
