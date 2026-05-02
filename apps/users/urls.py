from django.urls import path
from .views import RegisterView, UserProfileView, UserPreferencesView, DeleteAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('preferences/', UserPreferencesView.as_view(), name='preferences'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
]
