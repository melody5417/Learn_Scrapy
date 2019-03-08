# coding=utf-8

# http://docs.python-requests.org/zh_CN/latest/index.html

import requests

URL_GET = "http://127.0.0.1:8000/ip"
URL_POST = "http://127.0.0.1:8000/post"
URL_GET = "http://127.0.0.1:8000/get"

def use_simple():
    response = requests.get(URL_GET)
    print(response.headers)

def use_params_post():
    response = requests.post(URL_POST, data= {'word':'hello'})
    print(response.content)

def use_params_get():
    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.get(URL_GET, params=payload)
    print(r.url)

    payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
    response = requests.get(URL_GET, params=payload)
    print(response.url)
    print(response.text)
    print(response.encoding)


if __name__ == '__main__':
    use_simple()

    use_params_post()

    use_params_get()
