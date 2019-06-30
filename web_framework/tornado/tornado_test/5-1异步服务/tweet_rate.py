# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time
import pymongo
from pymongo import MongoClient


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('a')
        # 实例化了一个Tornado的HTTPClient类
        client = tornado.httpclient.HTTPClient()
        # 调用对象的fetch方法。fetch方法的同步版本使用要获取的URL作为参数。
        # rpp参数指定我们想获得搜索结果首页的100个推文，而result_type参数指定我们只想获得匹配搜索的最近推文
        # fetch方法会返回一个HTTPResponse对象
        response = client.fetch("http://gc.ditu.aliyun.com/geocoding?a={}".format(query))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        lon = body['lon']
        lat = body['lat']
        self.write("""
            <div style="text-align: center">
                <div style="font-size: 72px">%s</div>
                <div style="font-size: 144px">%.02f</div>
                <div style="font-size: 24px">tweets per second</div>
            </div>""" % (query, lat)
                   )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
