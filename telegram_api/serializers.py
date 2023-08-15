from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('chat_id', )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', )


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'timestamp')
