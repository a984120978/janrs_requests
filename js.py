import time

import requests
from lxml.etree import HTML
from model.Model import Ip, session


def request(method, url, proxies, data={}):
    if method == 'get':
        try:
            r = requests.get(url, proxies=proxies)
            return r
        except:
            return False
    try:
        requests.post(url, data, proxies=proxies)
    except:
        pass


def get_ip():
    for i in session.query(Ip).all():
        try:
            requests.get('http://www.baidu.com', proxies={'http': f'http://{i.ip}:{i.port}'}, timeout=5)
        except:
            continue
        main({'http': f'http://{i.ip}:{i.port}'})


def main(proxies):
    num = 1
    while True:
        url = f'https://janrs.com/category/%E6%89%80%E6%9C%89%E6%96%87%E7%AB%A0/page/{num}/'
        r = request('get', url, proxies)
        if r.status_code != 200:
            return
        html = HTML(r.text)
        urls = html.xpath('/html/body/div[2]/div/div/div[1]')[0]
        if len(urls) == 2:
            # 已经没有页面了
            return
        # 最后一个是下一页不处理
        for i in urls[:-1]:
            url = i[1][0].attrib['href']
            r = request('get', url, proxies)
            if not r:
                return
            html = HTML(r.text)
            u_id = html.xpath('//*[@id="thumbs"]')[0].attrib['data-id']
            data = {
                'action': 'love',
                'um_id': u_id,
                'um_action': 'love'
            }
            request('post', 'https://janrs.com/wp-admin/admin-ajax.php', proxies, data)
        num += 1


if __name__ == '__main__':
    while True:
        get_ip()
        time.sleep(60)
