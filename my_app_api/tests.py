from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from my_app_api.views import ConversationViewSet
from my_app_api.models import Conversation, Visitor
from my_app_api.serializers import ConversationSerializer
from my_app_api.views import ArticleViewSet
from my_app_api.models import Article
from my_app_api.views import UserViewSet
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from my_app_api.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from my_app_api.models import User, Conversation, Message, Visitor, Product
from my_app_api.serializers import UserSerializer, ConversationSerializer, MessageSerializer, VisitorSerializer, ProductSerializer
import uuid

class ArticleViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ArticleViewSet.as_view({'get': 'retrieve'})
        self.article = Article.objects.create(title='Test Article', content='Test Content')

    def test_retrieve(self):
        request = self.factory.get('/api/articles/{}/'.format(self.article.pk))
        response = self.view(request, pk=self.article.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Article')
        self.assertEqual(response.data['content'], 'Test Content')
        
class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.url = reverse('user-list')

    def test_create_user(self):
        data = {'email': 'new@example.com', 'first_name': 'Jane','last_name': 'doe', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class PasswordResetViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.url = reverse('password_reset')

    def test_create_password_reset(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email(self):
        data = {'email': 'invalid@example.com'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ConversationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.visitor = Visitor.objects.create(ip_address='127.0.0.1')
        self.url = reverse('conversation-list')

    def test_create_conversation_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_create_conversation_visitor(self):
        data = {'visitor_uuid': str(self.visitor.uuid)}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)

class MessageViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.conversation = Conversation.objects.create(user=self.user)
        self.url = reverse('message-list')

    def test_create_message(self):
        self.client.force_authenticate(user=self.user)  # Authentifiez l'utilisateur avant de créer un message
        data = {'conversation': self.conversation.id, 'text': 'bonjour je cherche un cadeau'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

