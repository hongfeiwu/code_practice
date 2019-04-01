# -*- coding: utf-8 -*-
"""
Werkzeug库的routing模块的主要功能在于URL解析

Rule类
Rule类继承自RuleFactory类。一个Rule的实例代表一个URL模式，一个WSGI应用可以处理很多不同的URL模式，这也就是说可以产生很多不同的Rule实例。
    empty() ——在实际情况中，Rule实例会和一个Map实例进行绑定。通过empty()方法可以将Rule实例和Map实例解除绑定。
    get_empty_kwargs() ——在empty()方法中调用，可以获得之前Rule实例的参数，以便重新构造一个Rule实例。
    get_rules(map) ——这个方法是对RuleFactory类中get_rules方法的重写，返回Rule实例本身。
    refresh() ——当修改Rule实例（URL规则）后可以调用该方法，以便更新Rule实例和Map实例的绑定关系。
    bind(map, rebind=False) ——将Rule实例和一个Map实例进行绑定，这个方法会调用complie()方法，会给Rule实例生成一个正则表达式。
    complie() ——根据Rule实例的URL模式，生成一个正则表达式，以便后续对请求的path进行匹配。
    match(path) ——将Rule实例和给定的path进行匹配。在调用complie()方法生成的正则表达式将会对path进行匹配。如果匹配，将返回这个path中的参数，以便后续过程使用。如果不匹配，将会由其他的Rule实例和这个path进行匹配。

Map类
通过Map类构造的实例可以存储所有的URL规则，这些规则是Rule类的实例。Map实例可以 通过后续的调用和给定的URL进行匹配。
    add(rulefactory) ——这个方法在构造Map实例的时候就会调用，它会将所有传入Map类中的Rule实例和该Map实例建立绑定关系。该方法还会调用Rule实例的bind方法。
    bind方法 ——这个方法会生成一个MapAdapter实例，传入MapAdapter的包括一些请求信息，这样可以调用MapAdapter实例的方法匹配给定URL。
    bind_to_environ方法 ——通过解析请求中的environ信息，然后调用上面的bind方法，最终会生成一个MapAdapter实例。

MapAdapter类
MapAdapter类执行URL匹配的具体工作。
    dispatch方法 ——该方法首先会调用MapAdapter实例的match()方法，如果有匹配的Rule，则会执行该Rule对应的视图函数。
    match方法 ——该方法将会进行具体的URL匹配工作。它会将请求中的url和MapAdapter实例中的所有Rule进行匹配，
    如果有匹配成功的，则返回该Rule对应的endpoint和一些参数rv。endpoint一般会对应一个视图函数，返回的rv可以作为参数传入视图函数中。
"""

from werkzeug.routing import Map, Rule, NotFound, RequestRedirect, HTTPException
url_map = Map([
    Rule('/', endpoint='blog/index'),
    Rule('/<int:year>/', endpoint='blog/archive'),
    Rule('/<int:year>/<int:month>/', endpoint='blog/archive'),
    Rule('/<int:year>/<int:month>/<int:day>/', endpoint='blog/archive'),
    Rule('/<int:year>/<int:month>/<int:day>/<slug>',
         endpoint='blog/show_post'),
    Rule('/about', endpoint='blog/about_me'),
    Rule('/feeds/', endpoint='blog/feeds'),
    Rule('/feeds/<feed_name>.rss', endpoint='blog/show_feed')
])


def application(environ, start_response):
    urls = url_map.bind_to_environ(environ)
    try:
        endpoint, args = urls.match()
    except HTTPException, e:
        return e(environ, start_response)
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Rule points to %r with arguments %r' % (endpoint, args)]

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)