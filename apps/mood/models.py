"""Mood tracking models for Serenity AI"""
from django.db import models
from django.conf import settings


class MoodLog(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Neutral'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    EMOTION_TAGS = [
        ('anxious', 'Anxious'),
        ('calm', 'Calm'),
        ('sad', 'Sad'),
        ('happy', 'Happy'),
        ('angry', 'Angry'),
        ('grateful', 'Grateful'),
        ('tired', 'Tired'),
        ('energized', 'Energized'),
        ('stressed', 'Stressed'),
        ('hopeful', 'Hopeful'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_logs')
    score = models.IntegerField(choices=MOOD_CHOICES)
    emotion_tags = models.JSONField(default=list)
    note = models.TextField(blank=True, null=True)
    energy_level = models.IntegerField(default=3)  # 1-5
    sleep_hours = models.FloatField(null=True, blank=True)
    
    # AI-generated fields
    ai_sentiment = models.CharField(max_length=20, blank=True)  # positive/negative/neutral
    ai_summary = models.TextField(blank=True)
    ai_triggers = models.JSONField(default=list)
    ai_processed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - Score {self.score} on {self.created_at.date()}"


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journal_entries')
    mood_log = models.OneToOneField(MoodLog, on_delete=models.SET_NULL, null=True, blank=True, related_name='journal')
    content = models.TextField()
    
    # AI-processed fields
    ai_themes = models.JSONField(default=list)
    ai_sentiment_score = models.FloatField(null=True, blank=True)  # -1 to 1
    ai_key_emotions = models.JSONField(default=list)
    ai_processed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Journal by {self.user.email} on {self.created_at.date()}"


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
