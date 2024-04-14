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
from my_app_api.models import Product, Favori, User, Gender, AgeRange, Occasion, Relationship, ActivityInterest, PersonalityPreference

from my_app_api.serializers import UserSerializer, ConversationSerializer, MessageSerializer, VisitorSerializer, ProductSerializer, FavoriSerializer
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

# class MessageViewSetTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='test@example.com', first_name='John')
#         self.conversation = Conversation.objects.create(user=self.user)
#         self.conversation.save()  # Sauvegardez explicitement la conversation
#         self.url = reverse('message-list')

#     def test_create_message(self):
#         self.client.force_authenticate(user=self.user)
#         data = {'conversation': self.conversation.id, 'text': 'bonjour je cherche un cadeau','type': 'Human'}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Message.objects.count(), 2)  # Vérifiez qu'il y a 2 messages (utilisateur et IA)

class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.gender = Gender.objects.create(name='Male')
        self.age_range = AgeRange.objects.create(age_range='Adult')
        self.occasion = Occasion.objects.create(occasion_name='Birthday')
        self.relationship = Relationship.objects.create(relationship_type='Friend')
        self.activity_interest = ActivityInterest.objects.create(activity='Sports')
        self.personality_preference = PersonalityPreference.objects.create(personality='Adventurous')
        self.product = Product.objects.create(name='Test Product', description='Test description', gender=self.gender)
        self.product.age_ranges.add(self.age_range)
        self.product.occasions.add(self.occasion)
        self.product.relationships.add(self.relationship)
        self.product.activities_interests.add(self.activity_interest)
        self.product.personalities_preferences.add(self.personality_preference)
        self.url = reverse('product-list')
        
    def test_list_products(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # def test_create_product(self):
    #     self.client.force_authenticate(user=self.user)
    #     gender = Gender.objects.create(name='Female')
    #     age_range = AgeRange.objects.create(age_range='Child')
    #     occasion = Occasion.objects.create(occasion_name='Christmas')
    #     relationship = Relationship.objects.create(relationship_type='Family')
    #     activity_interest = ActivityInterest.objects.create(activity='Reading')
    #     personality_preference = PersonalityPreference.objects.create(personality='Introverted')
    #     data = {
    #         'name': 'New Product',
    #         'description': 'New description',
    #         'gender': gender.id,
    #         'age_ranges': [age_range.id],
    #         'occasions': [occasion.id],
    #         'relationships': [relationship.id],
    #         'activities_interests': [activity_interest.id],
    #         'personalities_preferences': [personality_preference.id]
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', args=[self.product.id])
        data = {
            'name': 'Updated Product',
            'description': 'Updated description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class FavoriViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', first_name='John')
        self.gender = Gender.objects.create(name='Male')
        self.product = Product.objects.create(name='Test Product', description='Test description', gender=self.gender)
        self.favori = Favori.objects.create(user=self.user, product=self.product)
        self.url = reverse('favori-list')

    def test_list_favoris(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        favoris = Favori.objects.all()
        serializer = FavoriSerializer(favoris, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_favori(self):
        self.client.force_authenticate(user=self.user)
        product = Product.objects.create(name='New Product', description='New description', gender=self.gender)
        data = {
            'product': product.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favori.objects.count(), 2)

    def test_retrieve_favori(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('favori-detail', args=[self.favori.id])
        response = self.client.get(url)
        serializer = FavoriSerializer(self.favori)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_favori(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('favori-detail', args=[self.favori.id])
        product = Product.objects.create(name='Updated Product', description='Updated description', gender=self.gender)
        data = {
            'product': product.id
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.favori.refresh_from_db()
        self.assertEqual(self.favori.product.name, 'Updated Product')

    def test_delete_favori(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('favori-detail', args=[self.favori.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favori.objects.count(), 0)