"""Mood tracking models for Serenity AI"""
from django.db import models
from django.conf import settings




class MoodLog(models.Model):
    mood = models.CharField(max_length=50)
    note = models.TextField(blank=True)
    ai_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





class MoodInsight(models.Model):
    PERIOD_CHOICES = [('weekly', 'Weekly'), ('monthly', 'Monthly')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_insights')
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    average_score = models.FloatField()
    dominant_emotions = models.JSONField(default=list)
    improvement_areas = models.JSONField(default=list)
    ai_summary = models.TextField()
    streak_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
