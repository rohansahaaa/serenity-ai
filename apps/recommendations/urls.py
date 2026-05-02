from django.urls import path
from .views import RecommendationsView, CompleteRecommendationView, PracticeLibraryView

urlpatterns = [
    path('', RecommendationsView.as_view(), name='recommendations'),
    path('library/', PracticeLibraryView.as_view(), name='practice_library'),
    path('<int:pk>/complete/', CompleteRecommendationView.as_view(), name='complete_recommendation'),
]
