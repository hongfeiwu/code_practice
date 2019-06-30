# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def hello(request):
    """

    :param request:  一个触发这个视图、包含当前Web请求信息的对象，是类django.http.HttpRequest的一个实例。
    :return:
    """
    return HttpResponse("He9llo world ! ")
