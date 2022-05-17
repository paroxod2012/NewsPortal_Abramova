import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper_.settings')

app = Celery('NewsPaper_')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_monday_8am': {
        'task': 'newsapp.tasks.weekly_send_for_subscribers',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}