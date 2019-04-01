# -*- coding: utf-8 -*-
# tasks.py

from celery import Celery
from celery.utils.log import get_task_logger
import time

app = Celery('tasks',  backend='redis://localhost:6379/0', broker='redis://localhost:6379/0') #配置好celery的backend和broker
app.config_from_object('celery_config')

# class MyTask(app.Task):
#     """
#     继承app.Task,可重写task成功以及是失败的信息
#     """
#     def on_success(self, retval, task_id, args, kwargs):
#         print 'task done: {}'.format(retval)
#         return super(MyTask, self).on_success(retval, task_id, args, kwargs)
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print 'task fail, reason: {0}'.format(exc)
#         return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)
#
#
# @app.task(base=MyTask)
# def add(x, y):
#     return x + y

logger = get_task_logger(__name__)


@app.task(bind=True)
def add_time(self, x, y):
    logger.info(self.request.__dict__)
    return x + y


@app.task(bind=True)
def test_mes(self):
    for i in range(1, 11):
        time.sleep(0.1)
        self.update_state(state="PROGRESS", meta={'p': i*10})
    return 'finish'


@app.task(bind=True)
def period_task(self):
    print ('period task done:{0}').format(str(self.request.id))
