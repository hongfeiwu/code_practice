# -*- coding: utf-8 -*-
from spyne.application import Application
# 加了rpc装饰器后，该方法将暴露给客户端调用者，同时声明了接受的参数以及返回结果的数据类型
from spyne.decorator import srpc
# spyne.service.ServiceBase是所有定义服务的基类
from spyne.service import ServiceBase
# The names of the needed types for implementing this service should be self-explanatory.
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger
from spyne.model.primitive import String
from spyne.protocol.soap import Soap11
# Our server is going to use HTTP as transport, It’s going to wrap the Application instance.
from spyne.server.wsgi import WsgiApplication
# step1: 定义一个Spyne服务
class HelloWorldService(ServiceBase):


    @srpc(String, UnsignedInteger, _returns=Iterable(String))
    def say_hello(name, times):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param name: the name to say hello to
        @param times: the number of times to say hello
        @return  When returning an iterable, you can use any type of python iterable. Here, we chose to use generators.
        """
        for i in range(times):
            yield u'Hello, %s' % name
# step2: Glue the service definition, input and output protocols
soap_app = Application([HelloWorldService], 'spyne.examples.hello.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())
# step3: Wrap the Spyne application with its wsgi wrapper
wsgi_app = WsgiApplication(soap_app)
if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server
    # configure the python logger to show debugging output
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")
    # step4:Deploying the service using Soap via Wsgi
    # register the WSGI application as the handler to the wsgi server, and run the http server
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()