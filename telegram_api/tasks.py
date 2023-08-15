from celery import shared_task
from django.conf import settings
import requests


@shared_task(name='send_message')
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
    }
    requests.post(url, json=data)
