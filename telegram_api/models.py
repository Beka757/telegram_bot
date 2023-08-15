import string
from random import choice

from django.db import models
from authorization.models import User


class Chat(models.Model):
    chat_id = models.CharField(max_length=255, verbose_name='Чат айди')
    token = models.CharField(max_length=255, verbose_name='Tokен')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.chat_id} - {self.token}'

    def generate_token(self):
        chars = string.digits
        return ''.join(choice(chars) for _ in range(12))

    def save(self, *args, **kwargs):
        self.token = self.generate_token()
        super().save(*args, **kwargs)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Список сообщений'

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
