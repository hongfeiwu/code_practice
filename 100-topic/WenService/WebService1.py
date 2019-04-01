# -*- coding: utf-8 -*-
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode, ByteArray
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import requests
import urllib
import os
import uuid
import sys
import base64
import shutil

import subprocess
from subprocess import PIPE, Popen


class SoapService(ServiceBase):

    @rpc(Integer, _returns=ByteArray)
    def say_helloo(self, attachment_id):
        """
        获取附件，并装换
        :param attachment_id: pms中的附件id
        :return: 附件
        """
        docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/11'  # 应填写绝对路径
        shutil.rmtree(docx_cache)  # 强制删除文件夹
        os.mkdir(docx_cache)  # 新建同名文件夹
        url_half = 'http://127.0.0.1:8069/web/binary/oa_saveas?' \
                   'model=ir.attachment&field=datas&filename_field=datas_fname&id='
        attachment_url = url_half + str(attachment_id)
        attach = requests.get(attachment_url)
        name = attach.headers['Content-Disposition'].split("''")[1]
        # # ，Url参数字符串中使用key = value键值对这样的形式来传参，键值对之间以 & 符号分隔，
        # # 如 / s?q = abc & ie = utf - 8。如果你的value字符串中包含了 = 或者 &，
        # # 那么势必会造成接收Url的服务器解析错误，因此必须将引起歧义的 & 和 = 符号进行转义，
        # # 也就是对其进行编码。
        # # Python进行URL解码
        # # file_name = urllib.unquote(name).split('.')[0]
        docx_path = docx_cache + name
        # pdf_path = docx_cache + uuid.uuid1().__str__() + '.pdf'
        with open(docx_path, 'wb+') as f:
            f.write(attach.content)
        # # 获取增加页眉后的文件内容
        pdf = open(docx_path, 'r+')
        pdf_content = pdf.read()
        pdf.close()
        # # self.docx2pdf(docx_path, pdf_path)
        # # web_url = 'http://172.28.1.188'
        return pdf_content  # 返回url

    # def docx2pdf(self, input, output):
    #     import win32com
    #     from win32com import client
    #     word = client.DispatchEx('Word.Application')
    #     word.Visible = 0
    #     docx = word.Documents.Open(FileName=input, ReadOnly=1)
    #     docx.ExportAsFixedFormat(output, 17)
    #     docx.Close()
    #     word.Quit()


application = Application(
    [SoapService],
    tns='tns',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8033, wsgi_app)
    server.serve_forever()
