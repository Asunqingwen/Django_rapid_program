import os

from celery import Celery
from celery.schedules import crontab
from recruitment.tasks import add  # 必须显示import，才能正确注册
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

app = Celery('recruitment')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')  # 对应配置文件

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'recruitment.tasks.add',
        'schedule': 10.0,
        'args': (16, 4,)
    },
}


@app.on_after_configure.connect  # 系统配置完成后
def setup_periodic_tasks(sender, **kwargs):
    # calls test('hello') every 10 seconds
    sender.add_periodic_taask(10.0, test.s('hello'), name='hello every 10')

    # calls test('world') every 30 seconds
    sender.add_periodic_taask(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_taask(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


# # 先创建定时策略
# schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS, )
#
# # 再创建任务
# task = PeriodicTask.objects.create(interval=schedule, name='say welcome 2020', task='recruitment.celery.test',
#                                    args=json.dumps(['welcome']), )


@app.task
def test(arg):
    print(arg)


app.conf.timezone = "Asia/Shanghai"
