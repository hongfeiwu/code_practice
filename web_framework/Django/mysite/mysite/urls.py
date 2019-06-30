# -*- coding: utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from . import view


"""
url可以接收四个参数，分别是两个必选参数：regex、view 和两个可选参数：kwargs、name，接下来详细介绍这四个参数。
    1、regex: 正则表达式，与之匹配的 URL 会执行对应的第二个参数 view。
    2、view: 用于执行与正则表达式匹配的 URL 请求。
    3、kwargs: 视图使用的字典类型的参数。当Django发现正则表达式匹配时，Django将调用指定的视图函数，
        使用HttpRequest对象作为第一个参数，并将正则表达式中的任何“捕获”值作为其他参数。
    4、name: 用来反向获取 URL。
"""

urlpatterns = [
    url(r'^$', view.hello),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^todos/', include('todos.urls', namespace="todos")),
    url(r'^admin/', admin.site.urls),
]
