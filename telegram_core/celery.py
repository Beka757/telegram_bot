import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'telegram_core.settings')

app = Celery('telegram_core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['telegram_api.tasks'])
