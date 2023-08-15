from django.urls import path
from .views import ChatViewSet, MessageViewSet, UserMessagesViewSet


urlpatterns = [
    path('post_chat/', ChatViewSet.as_view({'post': 'create'})),
    path('post_message/', MessageViewSet.as_view({'post': 'create'})),
    path('get_messages/', UserMessagesViewSet.as_view({'get': 'list'})),
]
