import requests
import json
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
start_url = "https://movie.douban.com/top250"

# 开始爬虫
def start(url):
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

    htmlXPath = etree.HTML(html)
    next_page = (htmlXPath.xpath("//div[@class='paginator']//span[@class='next']/a/@href")[:1] or [None])[0]
    if next_page:
        next_url = start_url + str(next_page)
        start(next_url)

# 抓取页面
def get_one_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# xpath提取
def parse_one_page(html):
    htmlXPath = etree.HTML(html)
    items = htmlXPath.xpath("//div[@class='article']//ol[@class='grid_view']/li")
    for item in items:
        content = item.xpath(".//div[@class='info']//div[@class='bd']//p[1]/text()")
        yield {
            'serial_number': (item.xpath(".//div[@class='item']//em/text()")[:1 or [None]])[0],
            'movie_name': item.xpath(".//div[@class='item']//span[@class='title'][1]/text()")[0],
            'introduce': "".join(content).replace('&nbsp;', '').replace('<br>', '\n').replace('\n', ''),
            'star': (item.xpath(".//div[@class='info']//div[@class='bd']//span[@class='rating_num']/text()")[:1] or [None])[0],
            'evalutate': (item.xpath(".//div[@class='info']//div[@class='bd']//span[4]/text()")[:1] or [None])[0],
            'describe': (item.xpath(".//div[@class='info']//div[@class='bd']//span[@class='inq']/text()")[:1] or [None])[0],
        }

# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    start(start_url)







