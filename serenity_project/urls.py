"""Serenity AI URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    
    # Auth
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('apps.users.urls')),
    
    # App APIs
    path('api/v1/mood/', include('apps.mood.urls')),
    path('api/v1/chat/', include('apps.chat.urls')),
    path('api/v1/recommendations/', include('apps.recommendations.urls')),
]
