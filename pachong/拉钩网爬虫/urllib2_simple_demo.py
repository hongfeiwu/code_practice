# -*- coding: utf-8 -*-
import urllib
import sys
import urllib2
import codecs
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8 ')


def urllib2_demo_1():
    # 最多接受三个参数 urlopen(url, data, timeout)，返回一个response对象
    # 第一个参数url即为URL，必要
    # 第二个参数data是访问URL时要传送的数据，默认为空None，非必要
    # 第三个timeout是设置超时时间，timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT，非必要
    response = urllib2.urlopen('https://www.lagou.com/')
    html = response.read()
    soup = BeautifulSoup(html)
    species = soup.find_all("div", class_="menu_main job_hopping")
    data = {}
    for item in species:
        data_detail = {}
        for detail in item.find_all('a'):
            data_detail[detail.string] = detail.attrs['href']
        kind = item.h2.contents[0].strip()
        data[kind] = data_detail
    fh = codecs.open("test.txt", 'w', 'utf-8')
    for key in data.keys():
        fh.write(key + '\r\n')
        for item in data[key].keys():
            fh.write('\t' + item + ' ' * (10 - len(item)) + '链接' + data[key][item] + '\n')
    fh.close()
urllib2_demo_1()



def urllib2_demo_2():
    request = urllib2.Request("https://www.lagou.com/")
    # urlopen第一个参数也可以传入一个request请求,
    # 它其实就是一个Request类的实例，构造时需要传入Url,Data等等的内容。
    response = urllib2.urlopen(request)
    the_page = response.read()

    print the_page


def urllib2_demo_3():  # POST
    
    url = 'https://passport.lagou.com/login/login.html'
    values = {
        'username': '15726818294',
        'password': 'Password01!'
    }
    # 一般的HTML表单，data需要编码成标准形式。然后做为data参数传到Request对象。
    data = urllib.urlencode(values)  # 编码工作
    req = urllib2.Request(url, data)  # 发送请求同时传data表单
    response = urllib2.urlopen(req)  # 接受反馈的信息
    the_page = response.read()  # 读取反馈的内容
    print the_page


def urllib2_demo_4(key):  # GET
    url = "https://www.lagou.com/jobs/list_%s?" \
          "city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=" \
          "true&labelWords=&suginput=" % (key)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/55.0.2883.95 Safari/537.36"
    response = urllib2.urlopen(url)
    html = response.read()
    print html



