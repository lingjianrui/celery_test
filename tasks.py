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
