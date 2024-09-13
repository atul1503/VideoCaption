import os
from celery import Celery
from videocaption import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videocaption.settings')

app = Celery('videocaption')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()