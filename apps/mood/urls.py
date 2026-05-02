from django.urls import path
from .views import (MoodLogCreateView, MoodLogListView, MoodTrendsView,
                    JournalEntryView, WeeklyInsightView)

urlpatterns = [
    path('log/', MoodLogCreateView.as_view(), name='mood_log_create'),
    path('logs/', MoodLogListView.as_view(), name='mood_log_list'),
    path('trends/', MoodTrendsView.as_view(), name='mood_trends'),
    path('journal/', JournalEntryView.as_view(), name='journal_entry'),
    path('insights/weekly/', WeeklyInsightView.as_view(), name='weekly_insight'),
]
