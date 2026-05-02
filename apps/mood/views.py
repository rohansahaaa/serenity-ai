"""Mood views - core logic for Serenity AI"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from collections import Counter

from .models import MoodLog, JournalEntry, MoodInsight
from .serializers import (MoodLogSerializer, MoodLogCreateSerializer,
                           JournalEntrySerializer, MoodInsightSerializer, MoodTrendSerializer)
from .tasks import analyze_mood_with_ai


class MoodLogCreateView(generics.CreateAPIView):
    """POST /api/v1/mood/log/ - Submit a mood check-in"""
    serializer_class = MoodLogCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        mood_log = serializer.save(user=self.request.user)
        # Trigger async AI analysis via Celery
        analyze_mood_with_ai.delay(mood_log.id)
        return mood_log

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mood_log = self.perform_create(serializer)
        return Response({
            "message": "Mood logged successfully. AI analysis in progress.",
            "id": mood_log.id,
            "score": mood_log.score,
            "created_at": mood_log.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)


class MoodLogListView(generics.ListAPIView):
    """GET /api/v1/mood/logs/ - List user's mood history"""
    serializer_class = MoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MoodLog.objects.filter(user=self.request.user)
        days = self.request.query_params.get('days', 30)
        since = timezone.now() - timedelta(days=int(days))
        return queryset.filter(created_at__gte=since)


class MoodTrendsView(APIView):
    """GET /api/v1/mood/trends/ - Mood trend data grouped by day/week/month"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'week')
        if period == 'week':
            days = 7
        elif period == 'month':
            days = 30
        else:
            days = 90

        since = timezone.now() - timedelta(days=days)
        logs = MoodLog.objects.filter(user=request.user, created_at__gte=since)

        # Group by date
        trend_data = {}
        for log in logs:
            date_key = log.created_at.date().isoformat()
            if date_key not in trend_data:
                trend_data[date_key] = {'scores': [], 'emotions': []}
            trend_data[date_key]['scores'].append(log.score)
            trend_data[date_key]['emotions'].extend(log.emotion_tags)

        trends = []
        for date, data in sorted(trend_data.items()):
            dominant = Counter(data['emotions']).most_common(1)
            trends.append({
                'date': date,
                'average_score': round(sum(data['scores']) / len(data['scores']), 2),
                'log_count': len(data['scores']),
                'dominant_emotion': dominant[0][0] if dominant else 'neutral',
            })

        # Summary stats
        all_scores = [log.score for log in logs]
        summary = {
            'total_logs': len(all_scores),
            'average_score': round(sum(all_scores) / len(all_scores), 2) if all_scores else 0,
            'streak_days': self._calculate_streak(request.user),
            'improvement': self._calculate_improvement(logs, period),
        }

        return Response({'trends': trends, 'summary': summary})

    def _calculate_streak(self, user):
        streak = 0
        check_date = timezone.now().date()
        while MoodLog.objects.filter(user=user, created_at__date=check_date).exists():
            streak += 1
            check_date -= timedelta(days=1)
        return streak

    def _calculate_improvement(self, logs, period):
        if len(logs) < 2:
            return 0
        mid = len(logs) // 2
        first_half_avg = sum(l.score for l in logs[mid:]) / max(len(logs) - mid, 1)
        second_half_avg = sum(l.score for l in logs[:mid]) / max(mid, 1)
        return round(((second_half_avg - first_half_avg) / first_half_avg) * 100, 1) if first_half_avg else 0


class JournalEntryView(generics.CreateAPIView):
    """POST /api/v1/mood/journal/ - Submit journal entry"""
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        from .tasks import analyze_journal_with_ai
        entry = serializer.save(user=self.request.user)
        analyze_journal_with_ai.delay(entry.id)


class WeeklyInsightView(APIView):
    """GET /api/v1/mood/insights/weekly/ - AI-generated weekly summary"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        since = timezone.now() - timedelta(days=7)
        logs = MoodLog.objects.filter(user=request.user, created_at__gte=since)
        insight = MoodInsight.objects.filter(
            user=request.user, period='weekly'
        ).order_by('-created_at').first()

        if insight:
            return Response(MoodInsightSerializer(insight).data)
        return Response({"message": "No weekly insight available yet. Keep logging your mood!"})
