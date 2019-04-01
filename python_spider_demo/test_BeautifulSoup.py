import requests
import json
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
start_url = "https://movie.douban.com/top250"

# 开始爬虫
def start(url):
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

    soup = BeautifulSoup(html, 'lxml')
    next_page = soup.find("span", class_="next").find("a")["href"]
    if next_page:
        next_url = start_url + next_page
        start(next_url)

# 抓取页面
def get_one_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# beautifulsoup提取
def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all(attrs={'class': 'item'})
    for item in items:
        yield {
            'serial_number': item.find('em').get_text(),
            'movie_name': item.find("span", class_="title").get_text(),
            'introduce': "".join(item.find('div', class_="bd").p.get_text()).replace('&nbsp;', '').replace('<br>', '\n').replace('\n', ''),
            'star': item.find("span", class_="rating_num").get_text(),
            'evalutate': item.find("div", class_="star").contents[7].get_text(),
            'describe': item.find("span", class_="inq").get_text(),
        }

# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    start(start_url)







