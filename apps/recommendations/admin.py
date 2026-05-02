from django.contrib import admin
from .models import MindfulnessPractice, UserRecommendation

@admin.register(MindfulnessPractice)
class MindfulnessPracticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'duration_minutes', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title',)

@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'practice', 'is_completed', 'rating', 'created_at')
    list_filter = ('is_completed',)
