# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone


"""
所有模块继承自django.db.models.Model
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):  # __str__ on Python 3
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def save(self, *args, **kwargs):
        """
        重写保存函数
        当批量creating 或updating 对象时没有变通方法，因为不会调用save()、pre_save和 post_save。
        :param args:
        :param kwargs:
        :return:
        """
        # do_something()
        super(Question, self).save(*args, **kwargs)  # Call the "real" save() method.
        # do_something_else()

    def delete(self, *args, **kwargs):
        """
        重写删除函数
        使用查询集批量删除对象时，将不会为每个对象调用delete() 方法
        为确保自定义的删除逻辑得到执行，你可以使用pre_delete 和/或post_delete 信号。
        :param args:
        :param kwargs:
        :return:
        """
        # do_something()
        super(Question, self).delete(*args, **kwargs)  # Call the "real" save() method.
        # do_something_else()


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):  # __str__ on Python 3
        return self.choice_text


class CommonInfo(models.Model):
    """
    CommonInfo 模型无法像一般的Django模型一样使用，因为它是一个抽象基类。
    当它被用来作为一个其他model的基类时，它的字段将被加入那些子类中
    """
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        """
        Meta类中abstract = True表示为抽象基类
        当一个抽象基类被创建的时候, Django把你在基类内部定义的 Meta 类作为一个属性使其可用。
        如果子类没有声明自己的Meta 类, 他将会继承父类的Meta.
        如果子类想要扩展父类的Meta类，它可以作为其子类。
        """
        abstract = True
        ordering = ['name']


class Student(CommonInfo):
    """
     Student 模型将有三个项：name, age 和 home_group。
     Student继承自抽象基类CommonInfo，自动添加CommonInfo的两个字段name, age
    """
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta):
        """
        继承抽象基类时，继承时，Django 会对抽象基类的 Meta类做一个调整：
        在设置 Meta属性之前，Django 会设置 abstract=False。

        这意味着抽象基类的子类本身不会自动变成抽象类。
        """
        db_table = 'student_info'
