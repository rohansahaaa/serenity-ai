from django.contrib import admin
from .models import MoodLog, JournalEntry


@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ('mood', 'created_at')
    search_fields = ('mood', 'note')


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
