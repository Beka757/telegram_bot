from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from .models import Chat, Message
from rest_framework import permissions
from .serializers import ChatSerializer, MessageSerializer, UserMessagesSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_message


class ChatViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Chat.objects.filter(user=user).exists():
            return Response({'message': 'Чат айди уже существует!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)
        return Response({'message': 'Чат айди удачно зарегестрирован!'}, status=status.HTTP_200_OK)


class MessageViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        message = f"{user.username}, я получил от тебя сообщение:\n{request.data.get('text')}"
        try:
            chat = get_object_or_404(Chat.objects.all(), user=user)
            send_message.delay(chat_id=chat.chat_id, message=message)
            return Response(status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response({'error': 'Чат не зарегестрирован!'}, status=status.HTTP_400_BAD_REQUEST)


class UserMessagesViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Message.objects.all()
    serializer_class = UserMessagesSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        user = request.user
        messages = Message.objects.filter(user=user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
