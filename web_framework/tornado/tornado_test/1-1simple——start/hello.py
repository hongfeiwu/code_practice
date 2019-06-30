# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

# 设置默认port, help='...',用户运行程序时使用了 --help 选项，程序将打印出所有你定义 的选项
# type=int 为参数port 的类型define函数的help参数中指定的文本。
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting')
        hello = self.get_argument('Hello')
        self.write(greeting + ', friendly user!  ' + hello)

    def write_error(self, status_code, **kwargs):
        # 使用自己的方法代替默认的错误响应，重写write_error方法即可
        self.write("Gosh darnit, user! You caused a %d error." % status_code)


if __name__ == "__main__":
    # 从命令行中读取设置，python hello.py --port=8001
    # tornado的options模块解析命令本行，即读取port = 8001，
    # 代替默认的8000，假如port参数的值不是type定义的类型时，抛出异常
    tornado.options.parse_command_line()
    # 它告诉Tonado应该用IndexHandler类来响应请求。
    # Tornado在元组中使用正则表达式来匹配HTTP请求的路径。起Web框架作用，处理请求
    # handlers参数为一个元组组成的列表，其中每个元组的第一个元素是一个用于匹配的正则表达式，第二个元素是一个RequestHanlder类。
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    # 一旦Application对象被创建，我们可以将其传递给Tornado的HTTPServe r对象，
    # 然后使用我们在命令行指定的端口进行监听（通过options对象取出） 起web server功能，类似于flask的WSGI
    # 最后在程序准备好接收HTTP 请求后，我们创建一个Tornado的IOLoop的实例。
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
