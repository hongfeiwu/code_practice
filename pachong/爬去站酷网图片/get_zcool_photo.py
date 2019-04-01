# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests
import os
import uuid
import threading

sum = 0

def start_request(url):
    print "【提示】正在抓取 - " + str(url)
    res = requests.get(url)
    if res.status_code == 200:
        res_html = res.content
        doc = BeautifulSoup(res_html)
        work_box = doc.find('div', class_={'work-list-box'})
        card_box_list = work_box.find_all('div', class_={'card-box'})
        for item in card_box_list:
            get_content(item)
    else:
        print "【文档获取失败】【状态为{}】 - {}".format(str(url), res.status_code)


def get_content(item):
    title_content = item.find("a", class_={'title-content'})
    avatar = item.find('span', class_={'user-avatar'})
    if title_content is not None and avatar is not None:
        title = title_content.text    # 作品标题
        author = avatar.find("a")["title"]   # 作者名字
        href = title_content['href']  # 作品url
        res = requests.get(href)
        if res.status_code == 200:
            # 获取所有的图片链接
            img_list = get_doc_img_links(res.content)
            path_str = "【{}】-【{}】-共【{}】张".format(author.encode('utf-8'),
                                                 title.encode('utf-8'),
                                                 str(len(img_list)))
            path_str_mk = '/Users/whf/dev/w_dev/python_practice/pachong/爬去站酷网图片/图片/' + name_encode(path_str)
            if not os.path.exists(path_str_mk):
                os.mkdir(path_str_mk)
            if path_str_mk is None:
                return
            else:
                for img_item in img_list:
                    download_img(img_item, path_str_mk)

        else:
            print "【文档获取失败】【状态为{}】 - {}".format(href, str(res.status_code))
    else:
        return


def name_encode(file_name):
    file_stop_str = ['\\', '/', '*', '?', ':', '"', '<', '>', '|']
    for item2 in file_stop_str:
        file_name = file_name.replace(item2, '-')
    return file_name


def download_img(url, path):
    global sum
    z_url = url.split("@")[0]
    hz = url.split(".")
    z_hz = hz[len(hz) - 1]
    res = requests.get(z_url)
    if res.status_code == 200:
        img_down_path = path + "/" + str(uuid.uuid1()) + "." + z_hz
        f = open(img_down_path, 'wb')
        f.write(res.content)
        f.close()
        print str(sum) + "【下载成功】 -  " + img_down_path
        sum += 1
    else:
        print"【IMG下载失败】【状态为{}】 - {}".format(z_url, str(res.status_code))


def get_doc_img_links(html):
    """
    获取作品详情页的图片url
    :param html: 获取作品详情页
    :return: 获取作品详情页图片url列表
    """
    doc = BeautifulSoup(html)
    work_box = doc.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    img_list = []
    for item in revs:
        img = item.find("img")
        if img is not None:
            img_url = img["src"]
            img_list.append(img_url)
        else:
            print "【提示】：没有图片"
            continue
    return img_list

if __name__ == '__main__':
    threads = []
    start_url_list = [
        'http://www.zcool.com.cn/?p=2#tab_anchor',
        'http://www.zcool.com.cn/discover/0!0!0!0!0!!!!-1!0!2',
        'http://www.zcool.com.cn/discover/0!0!0!0!0!!!!-1!100!2'
    ]

    for start_url in start_url_list:
        threads.append(threading.Thread(target=start_request, args={start_url}))

    for item in threads:
        item.start()
