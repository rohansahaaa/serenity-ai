"""Users app models - Custom User for Serenity AI"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('therapist', 'Therapist'),
        ('admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    date_of_birth = models.DateField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    notification_enabled = models.BooleanField(default=True)
    onboarding_complete = models.BooleanField(default=False)
   # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"


class UserPreferences(models.Model):
    PRACTICE_TYPES = [
        ('meditation', 'Meditation'),
        ('breathing', 'Breathing'),
        ('journaling', 'Journaling'),
        ('movement', 'Movement'),
        ('soundscape', 'Soundscape'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    preferred_practices = models.JSONField(default=list)
    reminder_time = models.TimeField(null=True, blank=True)
    weekly_goal_minutes = models.IntegerField(default=30)
    theme = models.CharField(max_length=20, default='light')
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return f"Preferences for {self.user.email}"
