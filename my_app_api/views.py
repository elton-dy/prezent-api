from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import User, Conversation, Message, Produit, Favori
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer, ProduitSerializer, FavoriSerializer
from .ai_handler import conversational_chat
from rest_framework.response import Response
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


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

    def create(self, request, *args, **kwargs):
        user_message = request.data.get('text', '')  # Obtenez le texte du message de l'utilisateur
        conversation_id = request.data.get('conversation', None)  # Obtenez l'ID de la conversation

        if not conversation_id:
            return Response({'error': 'Conversation ID is required'}, status=400)

        try:
            conversation = Conversation.objects.get(pk=conversation_id)  # Récupérez l'objet Conversation
        except Conversation.DoesNotExist:
            return Response({'error': 'Invalid Conversation ID'}, status=400)

        # Créez le message utilisateur dans la base de données
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:  # Si le message de l'utilisateur a été créé avec succès
            ai_response = conversational_chat(user_message, conversation)  # Obtenez la réponse de l'IA

            # Créez le message de l'IA dans la base de données
            Message.objects.create(
                conversation=conversation,
                text=ai_response,
                type="AI"
            )
            return Response({'AI Response': ai_response}, status=201)

        return response  # Retournez la réponse HTTP originale

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class FavoriViewSet(viewsets.ModelViewSet):
    queryset = Favori.objects.all()
    serializer_class = FavoriSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)