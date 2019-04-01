# -*- coding: utf-8 -*-
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode, ByteArray
from spyne.protocol.soap import Soap11
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

docx_cache = '/Users/whf/dev/w_dev/python_practice/python/WenService/11/'  # 应填写绝对路径
pms_url = 'http://127.0.0.1:8069/'


# step1: Defining a Spyne Service
class WebServicePdf(ServiceBase):

    @rpc(Unicode, Integer, _returns=ByteArray)
    def ConvertPdf(self, name, attr_id):

        # 返回二进制内容，spyne会自动进行base64.encodestring，客户端需要进行base64.b64decode
        global docx_cache, pms_url
        self.create_cache_folder()
        odoo_response = self.get_odoo_attr(attr_id)

        name = odoo_response.headers['Content-Disposition'].split("''")[1]
        file_full_name = urllib.unquote(name)  # Python进行URL解码
        input_path = docx_cache + file_full_name
        pdf_path = docx_cache + uuid.uuid1().__str__() + '.pdf'
        with open(input_path, 'wb+') as f:     # 存储odoo附件
            f.write(odoo_response.content)

        file_type = urllib.unquote(name).split('.')[-1]
        if file_type in ['DOCX', 'docx']:     # 判断附件类型
            pass
            # self.docx2pdf(input_path, pdf_path)
        else:
            pdf_path = input_path

        # 获取增加页眉后的文件内容
        pdf = open(pdf_path, 'r+')
        pdf_content = pdf.read()
        pdf.close()

        return pdf_content

    def docx2pdf(self, input, output):
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

    def get_odoo_attr(self, attr_id):
        global pms_url
        attachment_url = pms_url + 'web/binary/oa_saveas?' \
                                   'model=ir.attachment&field=datas&' \
                                   'filename_field=datas_fname&id=' + str(attr_id)
        odoo_response = requests.get(attachment_url)
        return odoo_response

    def create_cache_folder(self):
        global docx_cache
        shutil.rmtree(docx_cache)  # 强制删除文件夹
        os.mkdir(docx_cache)  # 新建同名文件夹

# step2: Glue the service definition, input and output protocols
soap_app = Application([WebServicePdf], 'spyne.examples.hello.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# step3: Wrap the Spyne application with its wsgi wrapper
wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 6556, wsgi_app)
    print 'server start'
    server.serve_forever()

