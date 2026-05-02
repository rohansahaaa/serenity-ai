from django.contrib import admin
from .models import MoodLog, JournalEntry, MoodInsight

@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'ai_sentiment', 'ai_processed', 'created_at')
    list_filter = ('score', 'ai_sentiment', 'ai_processed')
    search_fields = ('user__email', 'note')
    readonly_fields = ('ai_sentiment', 'ai_summary', 'ai_triggers', 'ai_processed')

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_processed', 'created_at')
    list_filter = ('ai_processed',)

@admin.register(MoodInsight)
class MoodInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'average_score', 'start_date', 'end_date')
