# -*- coding: utf-8 -*-
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne.decorator import srpc
from spyne import Iterable, Integer, Unicode, ByteArray
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger
from spyne.model.primitive import String
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.protocol.msgpack import MessagePackDocument
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


# step1: Defining a Spyne Service
class WorldService(ServiceBase):

    @rpc(Unicode, Integer, _returns=ByteArray)
    def say_hello(self, name, times):
        docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/11/'  # 应填写绝对路径
        shutil.rmtree(docx_cache)  # 强制删除文件夹
        os.mkdir(docx_cache)  # 新建同名文件夹
        url_half = 'http://127.0.0.1:8069/web/binary/oa_saveas?' \
                   'model=ir.attachment&field=datas&filename_field=datas_fname&id='
        attachment_url = url_half + str(times)
        attach = requests.get(attachment_url)
        name = attach.headers['Content-Disposition'].split("''")[1]
        # # ，Url参数字符串中使用key = value键值对这样的形式来传参，键值对之间以 & 符号分隔，
        # # 如 / s?q = abc & ie = utf - 8。如果你的value字符串中包含了 = 或者 &，
        # # 那么势必会造成接收Url的服务器解析错误，因此必须将引起歧义的 & 和 = 符号进行转义，
        # # 也就是对其进行编码。
        # # Python进行URL解码
        file_name = urllib.unquote(name)
        docx_path = docx_cache + file_name
        # pdf_path = docx_cache + uuid.uuid1().__str__() + '.pdf'
        with open(docx_path, 'wb+') as f:
            f.write(attach.content)
        # # 获取增加页眉后的文件内容
        pdf = open(docx_path, 'r+')
        pdf_content = pdf.read()
        pdf.close()
        # self.docx2pdf(docx_path, pdf_path)
        # 返回二进制内容，spyne会自动进行base64.encodestring，客户端需要进行base64.b64decode
        return pdf_content

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def saysss_hello(self, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

    @rpc(Unicode, Integer,  _returns=Iterable(Unicode))
    def convert_to_pdf(self, name, times):
        # docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/11/'  # 应填写绝对路径
        # shutil.rmtree(docx_cache)  # 强制删除文件夹
        # os.mkdir(docx_cache)  # 新建同名文件夹
        # url_half = 'http://127.0.0.1:8069/web/binary/oa_saveas?' \
        #            'model=ir.attachment&field=datas&filename_field=datas_fname&id='
        # attachment_url = url_half + str(times)
        # attach = requests.get(attachment_url)
        # name = attach.headers['Content-Disposition'].split("''")[1]
        # # # ，Url参数字符串中使用key = value键值对这样的形式来传参，键值对之间以 & 符号分隔，
        # # # 如 / s?q = abc & ie = utf - 8。如果你的value字符串中包含了 = 或者 &，
        # # # 那么势必会造成接收Url的服务器解析错误，因此必须将引起歧义的 & 和 = 符号进行转义，
        # # # 也就是对其进行编码。
        # # # Python进行URL解码
        # file_name = urllib.unquote(name)
        # docx_path = docx_cache + file_name
        # # pdf_path = docx_cache + uuid.uuid1().__str__() + '.pdf'
        # with open(docx_path, 'wb+') as f:
        #     f.write(attach.content)
        # # # 获取增加页眉后的文件内容
        # pdf = open(docx_path, 'r+')
        # pdf_content = pdf.read()
        # pdf.close()
        # self.docx2pdf(docx_path, pdf_path)
        # 返回二进制内容，spyne会自动进行base64.encodestring，客户端需要进行base64.b64decode
        for i in range(times):
            yield u'Hello, %s' % name

# step2: Glue the service definition, input and output protocols
soap_app = Application([WorldService], 'spyne.examples.hello.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# step3: Wrap the Spyne application with its wsgi wrapper
wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':

    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8033, wsgi_app)
    print "listening to http://127.0.0.1:8033"
    print "wsdl is at: http://localhost:8033/?wsdl"
    server.serve_forever()

