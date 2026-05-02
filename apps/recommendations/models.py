"""Recommendations models for Serenity AI"""
from django.db import models
from django.conf import settings


class MindfulnessPractice(models.Model):
    CATEGORY_CHOICES = [
        ('meditation', 'Meditation'),
        ('breathing', 'Breathing Exercise'),
        ('journaling', 'Journaling'),
        ('movement', 'Mindful Movement'),
        ('soundscape', 'Soundscape'),
        ('visualization', 'Visualization'),
        ('grounding', 'Grounding Exercise'),
    ]
    DIFFICULTY_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_minutes = models.IntegerField()
    mood_tags = models.JSONField(default=list)
    instructions = models.TextField(blank=True)
    audio_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"


class UserRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    practice = models.ForeignKey(MindfulnessPractice, on_delete=models.CASCADE)
    reason = models.TextField()
    mood_score_at_time = models.IntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
