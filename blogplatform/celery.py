import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogplatform.settings')
app = Celery('blogplatform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# celery beat tasks

app.conf.beat_schedule = {
    'send-interesting-posts-every-5-minutes': {
        'task': 'blog.tasks.send_beat_email',
        'schedule': crontab(0,0,day_of_week='mon'),
    },
}