# -*- coding: utf-8 -*-
"""
这是一个简单的爬去赶集网的脚本
"""
import sys
import urllib2
from bs4 import BeautifulSoup
import random


reload(sys)
sys.setdefaultencoding('utf-8 ')
SHANGHAI_GJ = "http://sh.ganji.com"


root_url = u'http://www.76xh.com/'
img_urls = u'http://www.76xh.com/tupian/'
begin_url = u'http://www.76xh.com/tupian/2051.html'
photo_path = u'下载的图片/'

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

proxies = {
    "http": "http://182.148.123.133:8080",
    "http": "http://121.227.133.195:8118",
    "http": "http://119.115.246.251:8080",
    "http": "http://182.92.156.85:8118",
    "http": "http://110.81.199.186:8123",
    "http": "http://220.161.39.209:8118",
}

pages = 0
photos_sum = 0


# 保存上海各区域的url
def get_photo(start_url):
    """
    获取URL
    :return: 野马
    """
    # 使用代理IP
    global pages, photos_sum

    req = urllib2.Request(start_url)
    print start_url
    req.headers["User-Agent"] = random.choice(USER_AGENTS)
    response = None
    try:
        response = urllib2.urlopen(req, timeout=10)
    except urllib2.URLError, e:
        pages += 1
        get_photo(img_urls + str(pages) + '.html')
        print img_urls + str(pages) + '.html'
    if response:
        html = response.read()
        soup = BeautifulSoup(html)
        species = soup.find_all('div', class_="pic_text")
        if species:
            half_img_url = species[0].find_all('img')[0].attrs['src']
            ima_name = half_img_url.split('/')[-1]
            image = open(photo_path + ima_name, 'wb')
            img_data = urllib2.urlopen(root_url + half_img_url).read()
            image.write(img_data)
            image.close()
            photos_sum += 1
            print '第{}张图片{}保存成功, '.format(photos_sum, ima_name)
            species = soup.find_all('p', class_="shangyitiao textHide")
            if len(species) == 1:
                next_url = species[0].find_all('a')[0].attrs['href']
                pages = int(next_url.split('/')[-1].split('.')[0])
                get_photo(next_url)
            else:
                print start_url + '该页无图片'
        else:
            pages += 1
            get_photo(img_urls + str(pages) + '.html')
            print img_urls + str(pages) + '.html'


get_photo(begin_url)



