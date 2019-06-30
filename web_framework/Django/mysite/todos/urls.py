# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'todos'
urlpatterns = [
    url(r'^$', views.list_todo, name='todo'),
    url(r'^addtodo/$', views.add_todo, name='add'),
    url(r'^todofinish/(?P<id>d+)/$', views.finish_todo, name='finish'),
    url(r'^todobackout/(?P<id>d+)/$', views.back_todo, name='backout'),
    url(r'^updatetodo/(?P<id>d+)/$', views.update_todo, name='update'),
    url(r'^tododelete/(?P<id>d+)/$', views.delete_todo, name='delete'),
]

