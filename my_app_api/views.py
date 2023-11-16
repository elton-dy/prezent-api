from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import User, Conversation, Message, Product, Favori , Visitor
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer, FavoriSerializer , VisitorSerializer , ProductSerializer
from .ai_handler import conversational_chat
from rest_framework.response import Response
from rest_framework import permissions
from user_agents import parse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        # Déterminez si la conversation est initiée par un utilisateur ou un visiteur
        if not request.user.is_authenticated:
            # Générer ou récupérer l'UUID du visiteur
            try:
                visitor_uuid = request.data.get('visitor_uuid')
                if visitor_uuid:
                    visitor = get_object_or_404(Visitor, uuid=visitor_uuid)
                    request.data['visitor'] = visitor.id
                else:
                    # Handle the case where visitor_uuid is not provided
                    return Response({'error': 'Visitor UUID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Visitor.DoesNotExist:
                return Response({'error': 'No visitor found with the provided UUID.'}, status=status.HTTP_404_NOT_FOUND)


            # Attribuez l'ID du visiteur à la conversation
            request.data['visitor'] = visitor.id
        else:
            request.data['user'] = request.user.id

        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            conversation = self.serializer_class().Meta.model.objects.get(pk=response.data['id'])
            Message.objects.create(
                conversation=conversation,
                text="Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                type="AI"
            )
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Assuming 'messages' is a reverse relation from Message to Conversation
        messages = Message.objects.filter(conversation=instance)
        message_serializer = MessageSerializer(messages, many=True)
        response_data = serializer.data
        response_data['messages'] = message_serializer.data
        return Response(response_data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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
            return Response({'ai_response': ai_response, 'type': 'AI' }, status=201)

        return response  # Retournez la réponse HTTP originale

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def create(self, request, *args, **kwargs):
        ip_address = self.get_client_ip(request)
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        visitor = Visitor.objects.create(
            ip_address = ip_address,
            browser = user_agent.browser.family,
            os = user_agent.os.family,
            device = user_agent.device.family
        )
        serializer = self.get_serializer(visitor)
        return Response(serializer.data, status=201)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class FavoriViewSet(viewsets.ModelViewSet):
    queryset = Favori.objects.all()
    serializer_class = FavoriSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)