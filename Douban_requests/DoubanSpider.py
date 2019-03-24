import requests
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
start_url = "https://movie.douban.com/top250"

def start(url):
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

    next_pattern = re.compile(r'next.*?href="(.*?)"/>')
    next_page = re.search(next_pattern, html)
    if next_page:
        next_url = start_url + next_page.group(1)
        start(next_url)

# 抓取页面
def get_one_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 正则提取
# 发现问题 最后解析出249个 why？ 因为第249条 没有inq
def parse_one_page(html):
    pattern = re.compile(
        r'item[\s\S]*?em.*?>([0-9]*?)</em>[\s\S]*?title.*?>(.*?)</span>[\s\S]*?bd[\s\S]*?"">([\s\S]*?)</p>[\s\S]*?rating_num.*">(.*?)</span>[\s\S]*?>(.*?)人评价[\s\S]*?inq.*?>(.*?)</span>')
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'serial_number': item[0],
            'movie_name': item[1],
            'introduce': "".join(item[2].replace('&nbsp;', '').replace('<br>', '\n').split()),
            'star': item[3],
            'evalutate': item[4],
            'describe': item[5]
        }

# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    start(start_url)







