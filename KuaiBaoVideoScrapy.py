# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
import pandas as pd
import random

# define
Proxy_Name = "kuaibao"
PathToExcelFile = "/Users/yiqiwang/Desktop/video_list.xlsx"
Column_Name = "文章链接"
PathToBrowsermobProxy = "/Users/yiqiwang/Downloads/browsermob-proxy-2.1.4/bin/browsermob-proxy"
User_Agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0",
              "Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2909.25 Safari/537.36"]

# funcs

def startServer(path):
    server = Server(path=path)
    server.start()
    return server

def startProxy(server, proxy_name):
    proxy = server.create_proxy()
    proxy.new_har(proxy_name, options={'captureHeaders': True, 'captureContent': True})
    return proxy

def startDriver(proxy):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--user-agent={user_agent}'.format(user_agent=User_Agent[0]))
    chrome_options.add_argument('--proxy-server={host}:{port}'.format(host="localhost", port=proxy.port))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def readFile(path):
    data_frame = pd.read_excel(PathToExcelFile)
    return data_frame[Column_Name]

def getPage(proxy, driver, h5Url, new):
    # open page
    print("start scrapying " + h5Url)
    driver.get(h5Url)

    # find element and click
    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "use.txp_svg_symbol.txp_svg_play"))
        )
    except:
        if new:
            getPage(proxy, driver, h5Url, new=False)
            print("scrapy error: " + url)
        return

    driver.find_element_by_css_selector("use.txp_svg_symbol.txp_svg_play").click()

    # fetch url
    video_url = ""
    while len(video_url) == 0:
        entries = proxy.har['log']['entries']
        reverseEntries = reversed(entries)
        for entry in reverseEntries:
            if len(video_url) != 0:
                break

            _url = entry['request']['url']
            _rsp = entry['response']
            _headers = _rsp['headers']

            for _header in _headers:
                if _header['name'] == 'Content-Type':
                    if (_header['value'] == 'application/octet-stream') or (_header['value'] == 'video/mp4'):
                        if ("mp4" in _url) or ("ugc" in _url):
                            video_url = _url
                            break

    print(video_url)

if __name__ == '__main__':
    server = startServer(PathToBrowsermobProxy)
    h5Urls = readFile(path=PathToExcelFile)
    for url in h5Urls[30:121]:
        proxy = startProxy(server, url)
        driver = startDriver(proxy)
        getPage(proxy=proxy, driver=driver, h5Url=url, new=True)

        proxy.close()
        driver.quit()