from celery import Celery

# 第一个参数是当前脚本的名字，第二个参数每个异步任务的存储地址，第三个参数是broker服务器的地址
# 这里用redis做为broker，也可以用RabbitMQ等做为broker
app = Celery('tasks', backend='redis://127.0.0.1', broker='redis://127.0.0.1')

@app.task
def add(x, y):
    return x + y
