import json
import requests, os


def download_pic(file, name, html):
    r = requests.get(html)
    filename = os.path.join(file, name + '.jpg')
    with open(filename, 'wb') as f:
        f.write(r.content)


url = 'http://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1'

res = requests.get(url)
json_data = json.loads(res.text)
data = json_data['data']
file_path = u'test/'
for i in data:
    aa = getattr(i, 'image_detail', None)
    if not aa:
        for p in i['image_detail']:
            print p['url']
            name = p['url'].split('/')[-1]
            download_pic(file_path, name, p['url'])