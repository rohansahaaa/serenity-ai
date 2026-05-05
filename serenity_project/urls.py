"""Serenity AI URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from serenity_project import frontend_views


urlpatterns = [

    # 🟢 Frontend Pages (your real website)
    path('', frontend_views.home, name='home'),
    path('dashboard/', frontend_views.dashboard, name='dashboard'),
    path('mood-page/', frontend_views.mood_page, name='mood_page'),
    path('chat-page/', frontend_views.chat_page, name='chat_page'),
    path('recommendations-page/', frontend_views.recommendations_page, name='recommendations_page'),
    path('journal-page/', frontend_views.journal_page, name='journal_page'),
    path('mood-history/', frontend_views.mood_history_page, name='mood_history'),

    # 🔐 Admin
    path('admin/', admin.site.urls),

    # 🔑 Authentication (JWT)
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('apps.users.urls')),

    # 📡 APIs (clean version)
    path('api/v1/mood/', include('apps.mood.urls')),
    path('api/v1/chat/', include('apps.chat.urls')),
    path('api/v1/recommendations/', include('apps.recommendations.urls')),
]
