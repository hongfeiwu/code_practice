# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests

import urllib2
import os
import uuid
import threading
#
# sum = 0
#
# main_url = 'http://www.polayoutu.com/'
#
# def start_request(url):
#     print "【提示】正在抓取 - " + str(url)
#     res = requests.get(url)
#     if res.status_code == 200:
#         res_html = res.content
#         doc = BeautifulSoup(res_html)
#         work_box = doc.find_all('div', class_={'module_collection'})
#         for item in work_box:
#             get_content(item)
#     else:
#         print "【文档获取失败】【状态为{}】 - {}".format(str(url), res.status_code)
#
#
# def get_content(item):
#     global main_url
#     avatar = main_url + item.find("a", class_={'avatar has_link'})['href']
#     img_url = item.find("img", class_={'full_res_image'})['src']
#
#     camera = item.find("div", class_={'gears'}).string
#     location = item.find("div", class_={'location'}).string
#
#     title_content = item.find('span', class_={'user-avatar'})
#     if title_content is not None and avatar is not None:
#         title = title_content.text    # 作品标题
#         author = avatar.find("a")["title"]   # 作者名字
#         href = title_content['href']  # 作品url
#         res = requests.get(href)
#         if res.status_code == 200:
#             # 获取所有的图片链接
#             img_list = get_doc_img_links(res.content)
#             path_str = "【{}】-【{}】-共【{}】张".format(author.encode('utf-8'),
#                                                  title.encode('utf-8'),
#                                                  str(len(img_list)))
#             path_str_mk = '/Users/whf/dev/w_dev/python_practice/pachong/爬去站酷网图片/图片/' + name_encode(path_str)
#             if not os.path.exists(path_str_mk):
#                 os.mkdir(path_str_mk)
#             if path_str_mk is None:
#                 return
#             else:
#                 for img_item in img_list:
#                     download_img(img_item, path_str_mk)
#
#         else:
#             print "【文档获取失败】【状态为{}】 - {}".format(href, str(res.status_code))
#     else:
#         return
#
#
# def name_encode(file_name):
#     file_stop_str = ['\\', '/', '*', '?', ':', '"', '<', '>', '|']
#     for item2 in file_stop_str:
#         file_name = file_name.replace(item2, '-')
#     return file_name
#
#
# def download_img(url, path):
#     global sum
#     z_url = url.split("@")[0]
#     hz = url.split(".")
#     z_hz = hz[len(hz) - 1]
#     res = requests.get(z_url)
#     if res.status_code == 200:
#         img_down_path = path + "/" + str(uuid.uuid1()) + "." + z_hz
#         f = open(img_down_path, 'wb')
#         f.write(res.content)
#         f.close()
#         print str(sum) + "【下载成功】 -  " + img_down_path
#         sum += 1
#     else:
#         print"【IMG下载失败】【状态为{}】 - {}".format(z_url, str(res.status_code))
#
#
# def get_doc_img_links(html):
#     """
#     获取作品详情页的图片url
#     :param html: 获取作品详情页
#     :return: 获取作品详情页图片url列表
#     """
#     doc = BeautifulSoup(html)
#     work_box = doc.find("div", class_={'work-show-box'})
#     revs = work_box.find_all("div", class_={'reveal-work-wrap'})
#     img_list = []
#     for item in revs:
#         img = item.find("img")
#         if img is not None:
#             img_url = img["src"]
#             img_list.append(img_url)
#         else:
#             print "【提示】：没有图片"
#             continue
#     return img_list
number = 37
seq = 1
half_url = 'http://ppe.oss-cn-shenzhen.aliyuncs.com/collections/'
file_path = 'pola图片/'


def start_get():
    global number, seq, start_url, file_path
    start_url = half_url + str(number) + '/' + str(seq) + '/full_res.jpg'
    try:
        response = requests.get(start_url, timeout=2)
        print start_url
        if response.status_code == 200:
            filename = file_path + str(number) + '-' + str(seq) + '.jpg'
            with open(filename, 'wb') as f:
                f.write(response.content)
            seq += 1
            print '文件{}保存成功'.format(filename)
        else:
            number += 1
            seq = 1
            if number < 85:
                start_get()
    except urllib2.URLError:
        number += 1
        seq = 1
        if number < 85:
            start_get()


if __name__ == '__main__':
    while number < 104:
        start_get()


