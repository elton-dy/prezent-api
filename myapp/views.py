from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            conversation = self.serializer_class().Meta.model.objects.get(pk=response.data['id'])
            Message.objects.create(
                conversation=conversation,
                text="Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                type="AI"
            )
        return response

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
