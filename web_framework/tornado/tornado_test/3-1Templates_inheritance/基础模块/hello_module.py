# -*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class BookModule(tornado.web.UIModule):
    class BookModule(tornado.web.UIModule):
        def render(self, book):
            return self.render_string(
                "modules/book.html",
                book=book,
            )

        def embedded_javascript(self):
            return "document.write(\"hi!\")"


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"/static/images/collective_intelligence.gif",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                },
                {
                    "title": "33333e",
                    "subtitle": "Bui1111cations",
                    "image": "/static/images/collective_intelligence.gif",
                    "author": "123123",
                    "date_added": 1123,
                    "date_released": "August 2007",
                    "isbn": "978-0-596-52932-1",
                    "description": "<p>This fascinating book demonstrates how you "
                                   "can build web applications to mine the enormous amount of data created by people "
                                   "on the Internet. With the sophisticated algorithms in this book, you can write "
                                   "smart programs to access interesting datasets from other web sites, collect data "
                                   "from users of your own applications, and analyze and understand the data once "
                                   "you've found it.</p>"
                }
            ]
        )

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 为了在你的模板中引用模块，你必须在应用的设置中声明它。ui_moudles参数期望一个模块名为键、类为值的字典输入来渲染它们。
    # 这个例子中ui_module字典里只有一项，它把到名为Hello的模块的引用和我们定义的HelloModule类结合了起来。
    # 当调用HelloHandler并渲染hello.html时，我们可以使用{% module Hello() %}模板标签来包含HelloModule类中render方法返回的字符串。
    app = tornado.web.Application(
        handlers=[(r'/', HelloHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        ui_modules={'Hello': HelloModule}
    )
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()