# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Todo


def list_todo(request):
    todolist = Todo.objects.filter(flag=1)
    finishtodos = Todo.objects.filter(flag=0)
    return render_to_response('simpleTodo.html',
                              {'todolist': todolist, 'finishtodos': finishtodos})


def finish_todo(request, id=''):
    todo = Todo.objects.get(id=id)
    if todo.flag == '1':
        todo.flag = '0'
        todo.save()
        return HttpResponseRedirect('/simpleTodo/')
    todolist = Todo.objects.filter(flag=1)
    return render_to_response('simpleTodo.html', {'todolist': todolist})


def back_todo(request, id=''):
    todo = Todo.objects.get(id=id)
    if todo.flag == '0':
        todo.flag = '1'
        todo.save()
        return HttpResponseRedirect('/simpleTodo/')
    todolist = Todo.objects.filter(flag=1)
    return render_to_response('simpleTodo.html', {'todolist': todolist})


def delete_todo(request, id=''):
    todo = get_object_or_404(Todo, id=id)
    if todo:
        todo.delete()
        return HttpResponseRedirect('/simpleTodo/')
    todolist = Todo.objects.filter(flag=1)
    return render_to_response('simpleTodo.html', {'todolist': todolist})


def add_todo(request):
    if request.method == 'POST':
        atodo = request.POST['todo']
        priority = request.POST['priority']
        todo = Todo(todo=atodo, priority=priority, flag='1')
        todo.save()
        todolist = Todo.objects.filter(flag='1')
        finishtodos = Todo.objects.filter(flag=0)
        return render_to_response('showtodo.html',
                                  {'todolist': todolist, 'finishtodos': finishtodos})
    else:
        todolist = Todo.objects.filter(flag=1)
        finishtodos = Todo.objects.filter(flag=0)
        return render_to_response('simpleTodo.html',
                                  {'todolist': todolist, 'finishtodos': finishtodos})


def update_todo(request, id=''):
    if request.method == 'POST':
        print 'ddd'
        atodo = request.POST['todo']
        priority = request.POST['priority']
        todo = Todo(todo=atodo, priority=priority, flag='1')
        todo.save()
        todolist = Todo.objects.filter(flag='1')
        finishtodos = Todo.objects.filter(flag=0)
        return render_to_response('simpleTodo.html',
                                  {'todolist': todolist, 'finishtodos': finishtodos})
    else:
        todo = get_object_or_404(Todo, id=id)
        return render_to_response('updatatodo.html', {'todo': todo})