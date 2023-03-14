import requests
from lxml.etree import HTML

num = 1
while True:
    url = f'https://janrs.com/category/%E6%89%80%E6%9C%89%E6%96%87%E7%AB%A0/page/{num}/'
    r = requests.get(url)
    html = HTML(r.text)
    urls = html.xpath('/html/body/div[2]/div/div/div[1]')[0]
    if len(urls) == 2:
        # 已经没有页面了
        exit()
    # 最后一个是下一页不处理
    for i in urls[:-1]:
        url = i[1][0].attrib['href']
        r = requests.get(url)
        print(f'以访问{url}')
        html = HTML(r.text)
        u_id = html.xpath('//*[@id="thumbs"]')[0].attrib['data-id']
        data = {
            'action': 'love',
            'um_id': u_id,
            'um_action': 'love'
        }
        requests.post('https://janrs.com/wp-admin/admin-ajax.php', data)
        print('以点赞')
    num += 1
