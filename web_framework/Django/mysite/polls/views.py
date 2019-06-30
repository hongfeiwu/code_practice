# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """返回最近的5个问题"""
    #     return Question.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        包含pub_date小于等于timezone.now的Question
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context))


def index(request):
    """
    常见的习惯是载入一个模板、填充一个context 然后返回一个含有模板渲染结果的HttpResponse对象
    render()函数将请求对象作为它的第一个参数，模板的名字作为它的第二个参数，一个字典作为它可选的第三个参数。
    return： 它返回一个HttpResponse对象，含有用给定的context 渲染后的模板。
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

#
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})


def detail(request, question_id):
    """
    get_object_or_404 等同于上述
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST 是一个类似字典的对象
        # request.POST['choice'] 以字符串形式返回选择的Choice的ID。 request.POST 的值永远是字符串。
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 重新显示该问题的表单
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 始终在成功处理 POST 数据后返回一个 HttpResponseRedirect ，
        # （合并上句） 这样可以防止用户点击“后退”按钮时数据被发送两次。
        # （合并至上一句）
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
