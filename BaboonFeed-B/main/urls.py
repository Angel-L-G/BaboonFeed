"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from chats.views import MessageViewSet, ChatViewSet
from files.views import FileViewSet
from accounts.views import RegisterViewSet, VerifyEmailView, LoginViewSet
from posts.views import PostViewSet
from groups.views import GroupChatViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupChatViewSet, basename='groupchat')
router.register(r'files', FileViewSet, basename='file')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterViewSet.as_view({'post': 'register'}), name='register'),  # Register
    path('api/login/', LoginViewSet.as_view({'post': 'login'}), name='login'),  # Login (JWT)
    path('api/verify-email/<str:user_email>/<str:uid>/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


