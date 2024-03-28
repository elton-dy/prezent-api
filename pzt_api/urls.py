"""
URL configuration for pzt_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from my_app_api.views import UserViewSet, ConversationViewSet, MessageViewSet,ProductViewSet, FavoriViewSet , VisitorViewSet ,LoginView, ArticleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from my_app_api.serializers import CustomTokenObtainPairSerializer

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'products', ProductViewSet)
router.register(r'favoris', FavoriViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('api/', include([
        path('api/login/', LoginView.as_view(), name='login'),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('', include(router.urls)),
    ])),
]