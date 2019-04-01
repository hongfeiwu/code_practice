#### Celery 本身不是任务队列，它是管理分布式任务队列的工具
 
- Tasks 任务  
    想在队列中进行的任务咯，一般由用户、触发器或其他操作将任务入队，然后交由 workers 进行处理。
- Brokers   存储任务队列       
    brokers 就是生产者和消费者存放/拿取产品的地方(队列)
- Workers   工作者    
    Celery 中的工作者，类似与生产/消费模型中的消费者，其从队列中取出任务并执行
- backend   结果储存    
    队列中的任务运行完后的结果或者状态需要被任务发送者知道，那么就需要一个地方储存这些结果
    
redis命令
    
    brew install redis # 安装redis
    brew services start redis   #  后台启动
    redis-server /usr/local/etc/redis.conf  前台启动
    
在 tasks.py 所在目录下运行:

    celery -A tasks worker --loglevel=info
  
    
运行脚本trigger.py
Celery状态：
- PENDING	任务等待中
- STARTED	任务已开始
- SUCCESS	任务执行成功
- FAILURE	任务执行失败
- RETRY	任务将被重试
- REVOKED	任务取消


