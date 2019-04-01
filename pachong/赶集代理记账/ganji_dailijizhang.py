# -*- coding: utf-8 -*-
"""
这是一个简单的爬去赶集网的脚本
"""
import sys
import urllib2
import codecs
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8 ')
SHANGHAI_GJ = "http://sh.ganji.com"


# 保存上海各区域的url
def ganji():
    """
    获取URL
    :return: 野马
    """
    url = SHANGHAI_GJ + '/bangongshizhuangxiu/'
    # 使用代理IP
    # content = get_content(url)
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    species = soup.find_all('a', class_="a-area")
    # data = {}
    for item in species:
        if item.em.string != '不限':
            daili_pages(item.em.string, item.attrs['href'])


# 搜索每个区的代理记账
def daili_pages(area, href):
    """
    同上
    :param area: 地区
    :param href: 链接
    :return: 空白
    """
    text_file = codecs.open("办公室装修-细节-1.txt", 'a', 'utf-8')
    i = 1
    text_file.write(area + '\n')
    text_file.close()
    # 获取每个区page列表
    url_page_list = url_pages(href)
    test = False
    for u_page in url_page_list:
        i = daili_detail(u_page, i)
        test = True
    if not test:
        return daili_pages(area, href)


# 获取某个page业中所包含的信息
def daili_detail(u_page, i):
    """
    撒大
    :param u_page: 椰树
    :param i: 没
    :return: 吕
    """
    test = False
    text_file = codecs.open("代理记账-细节-1.txt", 'a', 'utf-8')
    response = urllib2.urlopen(u_page)
    html = response.read()
    soup = BeautifulSoup(html)
    species_img = soup.find_all('li', class_="list-img")
    species_noimg = soup.find_all('li', class_="list-noimg")
    for item in species_img:
        company_name = item.find_all('p', class_="p2")[0].a.string
        detail_url = item.find_all('p', class_="t")[0].a.attrs['href']
        telephone_number = url_detail(detail_url)
        if telephone_number != 0:
            text_file.write('\t' + company_name + '  电话：' + telephone_number + ' \n')
            test = True
    for item in species_noimg:
        nothing_href = item.find_all('p')[0].a.attrs['href']
        telephone_number = url_detail(nothing_href)
        if telephone_number != 0:
            text_file.write('\t' + '个人' + str(i) + '  电话：' + telephone_number + ' \n')
            i += 1
            test = True
    if not test:
        return daili_detail(u_page, i)
    text_file.close()


def url_pages(href):
    """
    所属
    :param href: 测试
    :return: 测试
    """
    url_list = []
    print SHANGHAI_GJ + href
    response = urllib2.urlopen(SHANGHAI_GJ + href)
    html = response.read()
    soup = BeautifulSoup(html)
    species_pages = []
    len_ul = len(soup.find_all('ul', class_="pageLink clearfix"))
    if len_ul > 0:
        species_pages = soup.find_all('ul', class_="pageLink clearfix")[0].find_all('a')
    len_species_pages = len(species_pages)
    if len_species_pages >= 1:
        url_list.append(SHANGHAI_GJ + href)
        for item in range(1, len(species_pages)-1):
            url_list.append(SHANGHAI_GJ + species_pages[item].attrs['href'])
    return url_list


def url_detail(detail_url):
    """
    撒大
    :param detail_url: 嗯嗯
    :return: 测试
    """
    re_2 = r"http.+"
    pattern2 = re.compile(re_2)
    c_url = len(pattern2.findall(detail_url))
    if c_url == 0:
        detail_url = SHANGHAI_GJ + detail_url
    else:
        detail_url = c_url[0]
    print detail_url
    detail_response = urllib2.urlopen(detail_url)
    detail_html = detail_response.read()
    detail_soup = BeautifulSoup(detail_html)
    class_name = "btn yahei displayphonenumber show_noauth_pop"
    len_a = len(detail_soup.find_all('a', class_=class_name))
    if len_a != 0:
        class_name = "btn yahei displayphonenumber show_noauth_pop"
        gjalog = detail_soup.find_all('a', class_=class_name)[0].attrs['gjalog']
        re_3 = r"(?<=@phone=).+?(?=@)"
        pattern3 = re.compile(re_3)
        telephone_number = pattern3.findall(gjalog)[0]
        return telephone_number

ganji()
