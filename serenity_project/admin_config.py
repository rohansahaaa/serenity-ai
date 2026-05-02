"""Admin configurations for Serenity AI"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser, UserPreferences
from apps.mood.models import MoodLog, JournalEntry, MoodInsight
from apps.chat.models import ChatSession, ChatMessage
from apps.recommendations.models import MeditationPractice, UserPracticeLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('Serenity Profile', {'fields': ('role', 'timezone', 'notification_enabled', 'onboarding_complete')}),
    )


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'weekly_goal_minutes', 'language')


@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'ai_sentiment', 'ai_processed', 'created_at')
    list_filter = ('score', 'ai_sentiment', 'ai_processed')
    search_fields = ('user__email',)
    readonly_fields = ('ai_sentiment', 'ai_summary', 'ai_triggers', 'ai_processed')
    date_hierarchy = 'created_at'


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_sentiment_score', 'ai_processed', 'created_at')
    list_filter = ('ai_processed',)
    search_fields = ('user__email', 'content')


@admin.register(MoodInsight)
class MoodInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'average_score', 'streak_days', 'created_at')
    list_filter = ('period',)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_active', 'created_at')
    list_filter = ('is_active',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'tokens_used', 'created_at')
    list_filter = ('role',)


@admin.register(MeditationPractice)
class MeditationPracticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'duration_minutes', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title', 'description')


@admin.register(UserPracticeLog)
class UserPracticeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'practice', 'completed', 'rating', 'created_at')
    list_filter = ('completed',)
