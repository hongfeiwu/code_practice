# -*- coding: utf-8 -*-
from suds.client import Client
import requests
import urllib
import os
import sys
import base64
import uuid

# web_url = 'http://172.28.1.188'
# url = 'http://192.168.2.172:8033/soap?wsdl'
# url = 'https://pms.pdmtr.com/soap?wsdl'
pms_url = 'http://10.100.1.168:8069/'
captcha = '814421e75fb762f1d6e0745298f0pe8d'

url = 'http://127.0.0.1:8001/convert/{0}?captcha={1}&pms_url={2}'.format(
    18440,
    captcha,
    pms_url)

# client = Client(url, timeout=3)
docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/cesh.pdf'
attach = requests.get(url).content
new_trans_file = open(docx_cache, 'a+')
new_trans_file.write(attach)
new_trans_file.close()
#
# pdf_url = client.service.say_hello('sdfs', 18440)
# new_trans_file = open(docx_cache, 'a+')
# new_trans_file.write(base64.b64decode(pdf_url))
# new_trans_file.close()
# client.service.saysss_hello('punk', 3)
# client.service.convert_to_pdf('sdfs', 3)
# pdf_url = client.service.convert_to_pdf('sdfs', 18440)
# docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/cesh.pdf'
# new_trans_file = open(docx_cache, 'a+')
# new_trans_file.write(base64.b64decode(pdf_url))
# new_trans_file.close()


# attach_response = requests.get(pdf_url)
# pdf_filepath = ''
# with open(pdf_filepath, 'wb') as f:
#     f.write(attach_response.content)
