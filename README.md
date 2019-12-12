
[TOC]

# 单个队列优先级(RabbitMQ)
**测试用例描述:**  
同一个队列 多个任务入queue，优先级高的先被消费   
**测试准备数据:**  
video_compress.apply_async(["a"], queue='tasks', priority=3)  
video_compress.apply_async(["b"], queue='tasks', priority=3)  
video_upload.apply_async(["c"], queue='tasks', priority=2)  
video_upload.apply_async(["d"], queue='tasks', priority=4) 
**预期测试结果:** 
命令行显示  
d  
a  
b  
c  
**测试方法:**    
1. python priority_test.py 将测试数据入queue
2. celery -A tasks worker -Q tasks --loglevel=info -c 1

**实际结果:**  
![](leanote://file/getImage?fileId=5df199c14da5dc0607000004)

# 多个队列优先级(RabbitMQ)
**测试用例描述:**  
多个队列，优先级高的先被消费，优先级低的后消费  
**测试准备数据:**  
video_compress.apply_async(["a"],queue='high')  
video_compress.apply_async(["b"],queue='low')  
video_upload.apply_async(["c"], queue='low')  
video_upload.apply_async(["d"], queue='high')  
**预期测试结果:**  
命令行显示  
a  
d  
b  
c  
**测试方法:**  
1. python multi_queue_priority_test.py 将测试数据入queue  
2. celery -A tasks worker -Q high,low --loglevel=info -c 1  

**实际结果:**  
![](leanote://file/getImage?fileId=5df197994da5dc0607000002)    

# 多个队列优先级混合单个队列优先级(RabbitMQ)  

**测试用例描述:**  
    多个普通队列带有优先级，和一个优先级队列在一起测试  

**测试准备数据:**  
    video_compress.apply_async(["a"],queue='highs', priority=8)    
    video_compress.apply_async(["b"],queue='low')  
    video_upload.apply_async(["c"], queue='low')  
    video_upload.apply_async(["d"], queue='highs',priority=1)    
 
**预期测试结果:**  
    命令行显示  
    a  
    d  
    b  
    c  

**测试方法:**  
1. python multi_single_queue_priority_test.py 将测试数据入queue  
2. celery -A tasks worker -Q highs,low --loglevel=info -c 1  

**实际结果:**  
![](leanote://file/getImage?fileId=5df199384da5dc0607000003)  


# 代码目录
celery_test  
├── celery_config.py  
├── multi_queue_priority_test.py  
├── multi_single_queue_priority_test.py  
├── priority_test.py  
└── tasks.py  

## celery_config.py  
```
from kombu import Exchange, Queue

CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_QUEUES = (
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
    Queue('highs', routing_key='highs', consumer_arguments={'x-priority': 5}, queue_arguments={'x-max-priority': 10}),
    Queue('high', routing_key='high', consumer_arguments={'x-priority': 5}),
    Queue('low', routing_key='low',consumer_arguments={'x-priority': 1}),
)
```
## multi_queue_priority_test.py
```
from tasks import video_compress, video_upload
if __name__ == '__main__':
    video_compress.apply_async(["a"],queue='high')
    video_compress.apply_async(["b"],queue='low')
    video_upload.apply_async(["c"], queue='low')
    video_upload.apply_async(["d"], queue='high')
```
## multi_single_queue_priority_test.py
```
from tasks import video_compress, video_upload
if __name__ == '__main__':
    video_compress.apply_async(["a"],queue='highs', priority=8)
    video_compress.apply_async(["b"],queue='low')
    video_upload.apply_async(["c"], queue='low')
    video_upload.apply_async(["d"], queue='highs', priority=1)
```
## priority_test.py
```
from tasks import video_compress, video_upload
if __name__ == '__main__':
    video_compress.apply_async(["a"],queue='tasks', priority=3)
    video_compress.apply_async(["b"],queue='tasks', priority=3)
    video_upload.apply_async(["c"], queue='tasks', priority=2)
    video_upload.apply_async(["d"], queue='tasks', priority=4)
```
## tasks.py
```
from celery import Celery
import time
import celery_config 
 
app = Celery('demo',broker='amqp://guest@localhost:5672')
app.config_from_object(celery_config)

 
# 视频压缩
@app.task
def video_compress(video_name):
    time.sleep(1)
    print('Compressing the:'+video_name)
    return 'success'
 
@app.task
def video_upload(video_name):
    time.sleep(1)
    print('Compressing the:'+video_name)
    return 'success'
```


