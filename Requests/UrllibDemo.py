# coding=utf-8

import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "http://127.0.0.1:8000/"

if __name__ == '__main__':
    # This page
    # response = urllib.request.urlopen(BASE_URL)
    # print(response.read().decode('utf-8'))

    # # ip
    # r = urllib.request.urlopen(BASE_URL+'ip')
    # print(r.read().decode('utf-8'))
    # # geturl 用于看是否重定向
    # print(r.geturl())
    # # info 返回元信息
    # print(r.info())
    # # getcode 返回回复的http状态码，成功是200
    # # 可以用来检查代理IP的可使用性
    # print(r.getcode())

    # # uuid
    # r = urllib.request.urlopen(BASE_URL + 'uuid')
    # print(r.read().decode('utf-8'))

    # # user-agent
    # # 可以让爬虫伪装成浏览器，而不被服务器发现你正在使用爬虫
    # r = urllib.request.urlopen(BASE_URL + 'user-agent')
    # print(r.read().decode('utf-8'))

    # # headers
    # # 有些网站设有反爬虫机制，检查请求若没有headers就会报错。
    # # 为保证爬虫的稳定性，每次都需设置headers。
    # r = urllib.request.urlopen(BASE_URL + 'headers')
    # print(r.read().decode('utf-8'))

    # # get
    # r = urllib.request.urlopen(BASE_URL + 'get')
    # print(r.read().decode('utf-8'))

    # #post
    # data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
    # r = urllib.request.urlopen(BASE_URL + 'post', data=data)
    # print(r.read().decode('utf-8'))

    # error
    # try:
    #     headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101  Firefox/57.0'}
    #     response = urllib.request.Request(BASE_URL, headers=headers)
    #     html = urllib.request.urlopen(response)
    #     result = html.read().decode('utf-8')
    # except urllib.error.URLError as e:
    #     if hasattr(e, 'reason'):
    #         print('reason' + str(e.reason))
    # except urllib.error.HTTPError as e:
    #     if hasattr(e, 'code'):
    #         print('code' + str(e.code))
    # else:
    #     print('success')

    # post
    # 豆瓣登陆


    # headers 信息，从fiddler上或你的浏览器上可复制下来
    headers = {'Accept': 'text/html,application/xhtml+xml,'
                         'application / xml,'
                         'q = 0.9, image / webp, image / apng,'
                         '* / *;q = 0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3;'
                          'Win64;'
                          'x64) AppleWebKit / 537.36'
                          '(KHTML, like Gecko)'
                          'Chrome / 48.0'
                          '.2564'
                          '.48'
                          'Safari / 537.36'
               }
    # POST请求的信息，填写你的用户名和密码
    value = {'source': 'index_nav',
    'form_password': '',
    'form_email': '@126.com'
    }
    try:
        data = urllib.parse.urlencode(value).encode('utf8')
        response = urllib.request.Request('https://www.douban.com/login', data=data, headers=headers)
        html = urllib.request.urlopen(response)
        result = html.read().decode('utf8')
        print(result)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('错误原因是' + str(e.reason))
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print('错误编码是' + str(e.code))
    else:
        print('请求成功通过。')

