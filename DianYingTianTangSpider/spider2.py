import requests
import json
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
start_url = "https://www.dygod.net/html/gndy/dyzz/"
detail_base_url = "https://www.dygod.net"
start_index = 1

# 开始爬虫
def start(url):
    html = get_one_page(url)
    for item in parse_list_page(html):
        write_to_file(item)

    # 在python的函数中和全局同名的变量，如果你有修改变量的值就会变成局部变量，
    # 在修改之前对该变量的引用自然就会出现没定义这样的错误了，
    # 如果确定要引用全局变量，并且要对它修改，必须加上global关键字
    global  start_index
    start_index = start_index + 1
    next_page = "index_{0}.html".format(str(start_index))

    if next_page and start_index < 3:
        next_url = start_url + str(next_page)
        start(next_url)

# 抓取页面
def get_one_page(url):
    print("url: " + url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("get_one_page succeed")
        return response.content.decode("gbk")
    else:
        print("get_one_page failed")
    return None

# xpath提取
def parse_list_page(html):
    htmlXPath = etree.HTML(html)
    items = htmlXPath.xpath("//div[@class='co_content8']//table")
    for item in items:
        title = item.xpath(".//a[@class='ulink']/text()")
        detail_link = detail_base_url + item.xpath(".//a[@class='ulink']/@href")[0]
        detail_html = get_one_page(detail_link)
        download_link = parse_detail_page(detail_html)
        yield {
            "title": title,
            "url": detail_link,
            "download_link": download_link
        }

def parse_detail_page(html):
    htmlXpath = etree.HTML(html)
    download_link = htmlXpath.xpath("//div[@id='Zoom']/table/tbody/tr/td/a/@href")
    return download_link


# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    start(start_url)







