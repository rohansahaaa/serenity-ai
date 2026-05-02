"""Mood serializers"""
from rest_framework import serializers
from .models import MoodLog, JournalEntry, MoodInsight


class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ('id', 'score', 'emotion_tags', 'note', 'energy_level',
                  'sleep_hours', 'ai_sentiment', 'ai_summary', 'ai_triggers',
                  'ai_processed', 'created_at')
        read_only_fields = ('ai_sentiment', 'ai_summary', 'ai_triggers', 'ai_processed', 'created_at')


class MoodLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ('score', 'emotion_tags', 'note', 'energy_level', 'sleep_hours')


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ('id', 'mood_log', 'content', 'ai_themes', 'ai_sentiment_score',
                  'ai_key_emotions', 'ai_processed', 'created_at')
        read_only_fields = ('ai_themes', 'ai_sentiment_score', 'ai_key_emotions', 'ai_processed', 'created_at')


class MoodInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodInsight
        fields = '__all__'
        read_only_fields = ('user',)


class MoodTrendSerializer(serializers.Serializer):
    date = serializers.DateField()
    average_score = serializers.FloatField()
    log_count = serializers.IntegerField()
    dominant_emotion = serializers.CharField()
