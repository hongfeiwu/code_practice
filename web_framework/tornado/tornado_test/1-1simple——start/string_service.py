# -*- coding: utf-8 -*-
import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        # input这个参数将包含匹配处理函数正则表达式第一个括号里的字 符串。
        self.write(input[::-1])

    def write_error(self, status_code, **kwargs):
        # 使用自己的方法代替默认的错误响应，可以重写write_error方法
        self.write("Gosh darnit, user! You caused a %d error." % status_code)


class WrapHandler(tornado.web.RequestHandler):
    # 但Tornado支持任何合法的HTTP请求（GET、POST、PUT、DELETE、HEAD、OPTIONS）。
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        # 使用Python内建的textwrap模块来以指定的宽度装饰文本，并将结果字符串写回到HTTP响应中。
        self.write(textwrap.fill(text, int(width)))
        # 显式地设置HTTP状态码。在某些情况下，Tornado会自动地设置HTTP状态码。
        # 1、404 Not Found
        #   Tornado会在HTTP请求的路径无法匹配任何RequestHandler类相对应的模式时返回404（Not Found）响应码。
        # 2、400 Bad Request
        #     如果你调用了一个没有默认值的get_argument函数，并且没有发现给定名称的参数，
        #     Tornado将自动返回一个400（Bad Request）响应码。
        # 3、405 Method Not Allowed
        #     如果传入的请求使用了RequestHandler中没有定义的HTTP方法（比如，一个POST请求，但是处理函数中只有定义了get方法），Tornado将返回一个405（Methos
        # Not Allowed）响应码。
        # 4、500 Internal Server Error
        #     当程序遇到任何不能让其退出的错误时，Tornado将返回500（Internal Server Error）响应码。
        #     你代码中任何没有捕获的异常也会导致500响应码。
        # 5、200 Ok
        #     如果响应成功，并且没有其他返回码被设置，Tornado将默认返回一个200（OK）响应码。
        self.set_status(200)


if __name__ == "__main__":

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        # (\w+)括号的含义是让Tornado保存匹配括号里面表达式的字符串，并将其作为请求方法的一个参数传递给RequestHandler类。
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
