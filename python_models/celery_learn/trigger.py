# -*- coding: utf-8 -*-

#trigger.py
from tasks import add_time, test_mes
import time
import sys

result = add_time.delay(4, 4)  # 不要直接 add(4, 4)，这里需要用 celery 提供的接口 delay 进行调用
while not result.ready():
    time.sleep(1)
print 'task done: {0}'.format(result.get())

def pm(body):
    res = body.get('result')
    if body.get('status') == 'PROGRESS':
        sys.stdout.write('\r任务进度: {0}%'.format(res.get('p')))
        sys.stdout.flush()
    else:
        print '\r'
        print res
r = test_mes.delay()
print r.get(on_message=pm, propagate=False)