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
        
class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({'get': 'list', 'post': 'create'})
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list(self):
        request = self.factory.get('/api/users/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_create(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').check_password('newpassword'), True)

    def test_create_unauthenticated(self):
        self.client.logout()
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='newuser').check_password('newpassword'), True)

    def test_list_unauthenticated(self):
        self.client.logout()
        request = self.factory.get('/api/users/')
        response = self.view(request)
        self.assertEqual(response.status_code, 401)
# Create your tests here.
