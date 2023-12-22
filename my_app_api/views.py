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
from .permissions import IsAuthenticatedOrVisitorWithUUID
from .permissions import CreateOrReadOnly

import re

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticatedOrVisitorWithUUID]

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
            initial_message = Message.objects.create(
                conversation=conversation,
                text="Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                type="AI"
            )

            message_serializer = MessageSerializer(initial_message)

            response_data = response.data
            response_data['messages'] = [message_serializer.data]
            return Response(response_data, status=status.HTTP_201_CREATED)
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
#     permission_classes = [IsAuthenticatedOrVisitorWithUUID]

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
            product_ids = self.extract_product_ids(ai_response)
            product_details = []
            for product_id in product_ids:
                try:
                    product = Product.objects.get(pk=product_id)
                    product_serializer = ProductSerializer(product)
                    product_details.append(product_serializer.data)
                except Product.DoesNotExist:
                    product_details.append({'error': f'Product with ID {product_id} not found'})

            # Créez le message de l'IA dans la base de données
            Message.objects.create(
                conversation=conversation,
                text=ai_response,
                type="AI"
            )
            cleaned_ai_response = self.clean_ai_response(ai_response)
            return Response({'ai_response': cleaned_ai_response, 'type': 'AI','product_details': product_details }, status=201)

        return response  # Retournez la réponse HTTP originale

    def extract_product_ids(self,ai_response):
            # Regex pour trouver un motif correspondant à l'ID de produit
            # Par exemple, elle cherche des chaînes qui ressemblent à "'id' => '89'"
            matches = re.findall(r"\'id\'\s*=>\s*'(\d+)'", ai_response)
            return matches if matches else []

    def clean_ai_response(self,ai_response):
        # Utilisez une expression régulière pour retirer les parties avec 'id' => 'valeur'
        cleaned_response = re.sub(r"\['id' => '\d+'\]", '', ai_response)
        return cleaned_response.strip()

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [CreateOrReadOnly]

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
#     permission_classes = [IsAuthenticatedOrVisitorWithUUID]


class FavoriViewSet(viewsets.ModelViewSet):
    queryset = Favori.objects.all()
    serializer_class = FavoriSerializer
#     permission_classes = [IsAuthenticatedOrVisitorWithUUID]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)