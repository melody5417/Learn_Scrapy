# coding=utf-8

import urllib.request
import urllib.parse

URL_IP = "http://127.0.0.1:8000/ip"
URL_GET = "http://127.0.0.1:8000/post"

def use_simple_urllib():
    response = urllib.request.urlopen(URL_IP)
    print(response.read().decode('utf-8'))

def use_params_urllib():
    data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
    response = urllib.request.urlopen(URL_GET, data=data)
    print(response.read().decode('utf-8'))


if __name__ == '__main__':
    # use_simple_urllib()

    use_params_urllib()