# -*- coding: utf-8 -*-
import sys
import urllib2
import codecs
import pdfkit
from bs4 import BeautifulSoup
import re

reload(sys)
sys.setdefaultencoding('utf-8 ')

url_dict = {
    "阮一峰git教程": "http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000",
    # "阮一峰python教程": "http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000#0"
}

class pachong(object):
    """
        基类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 保存的pdf文件名
        :param start_url: 爬虫入口url
        """
        self.name = name
        self.start_url = start_url



def parse_url_to_html(url, title):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    body = soup.find_all(class_="x-wiki-content")[0]
    html = str(body)
    re_h = re.compile('h[0-9]')  # 匹配h标签
    re_p = re.compile('p')  # 匹配p标签
    html = re_h.sub('a', html)
    html = re_p.sub('a', html)
    html = "<h3>" + str(title) + "<h3>" + html
    aa.write(html)
    return html


def get_url_list(url):
    """
    获取所有URL目录列表
    """
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    i=0
    for li in menu_tag.find_all("li"):
        i += 1
        if i < 6:
            url = "http://www.liaoxuefeng.com" + li.a.get('href')
            print li.a.string + url
            parse_url_to_html(url, li.a.string)


def save_pdf(name):
    """
    把所有html文件转换成pdf文件
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    pdfkit.from_file("%s.html" % name, '%s.pdf' % name, options=options)


for item in url_dict.keys():
    aa = open("%s.html" % item, 'wb')
    get_url_list(url_dict[item])
    save_pdf(item)
    aa.close()


