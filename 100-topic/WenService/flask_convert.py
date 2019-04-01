# -*- coding: utf-8 -*-
from flask import Flask
from flask import send_file, send_from_directory
import os
from flask import make_response
from flask import request
import requests
import urllib
import os
import uuid
import sys
import base64
import shutil

import subprocess
from subprocess import PIPE, Popen

app = Flask(__name__)


AuthorizationCode = '814421e75fb762f1d6e0745298f0pe8d'
docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/11/'  # 应填写绝对路径

def docx2pdf(input, output):
    import win32com
    from win32com import client
    # Dispatch() 在创建对象实例前会尝试使用GetObject(),如果有运行的实例,会得到该实例对象;
    # DispatchEx（）直接创建一个对象实例.
    word = client.DispatchEx('Word.Application')
    word.Visible = 0
    docx = word.Documents.Open(FileName=input, ReadOnly=1)
    docx.ExportAsFixedFormat(output, 17)
    docx.Close()
    word.Quit()


def get_odoo_attr(pms_url, attr_id):
    attachment_url = pms_url + 'web/binary/oa_saveas?' \
                               'model=ir.attachment&field=datas&' \
                               'filename_field=datas_fname&id=' + str(attr_id)
    odoo_response = requests.get(attachment_url)
    return odoo_response


def create_cache_folder():
    global docx_cache
    shutil.rmtree(docx_cache)  # 强制删除文件夹
    os.mkdir(docx_cache)  # 新建同名文件夹


@app.route('/')
def index():
    return 'Index Page'


@app.route('/convert/<int:attr_id>')
def convert_docx_pdf(attr_id):
    """
    获取odoo附件并进行转换
    :param attr_id:
    :return:
    """
    captcha = request.args.get('captcha')
    pms_url = request.args.get('pms_url')
    if captcha != AuthorizationCode:
        return '验证码不正确。'

    global docx_cache
    create_cache_folder()
    odoo_response = get_odoo_attr(pms_url, attr_id)

    name = odoo_response.headers['Content-Disposition'].split("''")[1]
    file_full_name = urllib.unquote(name)  # Python进行URL解码
    input_path = docx_cache + file_full_name

    with open(input_path, 'wb+') as f:  # 存储odoo附件
        f.write(odoo_response.content)

    pdf_name = uuid.uuid1().__str__() + '.pdf'
    pdf_path = docx_cache + pdf_name
    file_type = urllib.unquote(name).split('.')[-1]
    if file_type in ['DOCX', 'docx']:  # 判断附件类型
        # pass
        docx2pdf(input_path, pdf_path)
    else:
        pdf_path = input_path

    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    response = make_response(send_from_directory(docx_cache, pdf_name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(pdf_name)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

