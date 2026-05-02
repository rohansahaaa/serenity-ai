from django.urls import path
from .views import ChatMessageView, ChatSessionListView, ChatHistoryView
from .views import mood_analysis_view



urlpatterns = [
    path('message/', ChatMessageView.as_view(), name='chat_message'),
    path('sessions/', ChatSessionListView.as_view(), name='chat_sessions'),
    path('mood/', mood_analysis_view),
    path('sessions/<int:session_id>/history/', ChatHistoryView.as_view(), name='chat_history'),
]
