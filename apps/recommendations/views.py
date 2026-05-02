"""Recommendations views"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.utils import timezone

from .models import MindfulnessPractice, UserRecommendation


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindfulnessPractice
        fields = ('id', 'title', 'description', 'category', 'difficulty',
                  'duration_minutes', 'mood_tags', 'instructions', 'audio_url')


class RecommendationSerializer(serializers.ModelSerializer):
    practice = PracticeSerializer(read_only=True)

    class Meta:
        model = UserRecommendation
        fields = ('id', 'practice', 'reason', 'mood_score_at_time',
                  'is_completed', 'completed_at', 'rating', 'created_at')


class RecommendationsView(APIView):
    """GET /api/v1/recommendations/ - Personalized recommendations based on mood"""
    permission_classes = [IsAuthenticated]

    MOOD_PRACTICE_MAP = {
        1: ['grounding', 'breathing', 'soundscape'],
        2: ['breathing', 'grounding', 'visualization'],
        3: ['meditation', 'journaling', 'movement'],
        4: ['meditation', 'movement', 'journaling'],
        5: ['movement', 'visualization', 'meditation'],
    }

    EMOTION_PRACTICE_MAP = {
        'anxious': ['breathing', 'grounding', 'soundscape'],
        'sad': ['visualization', 'journaling', 'soundscape'],
        'angry': ['breathing', 'movement', 'grounding'],
        'stressed': ['breathing', 'meditation', 'soundscape'],
        'calm': ['meditation', 'visualization', 'journaling'],
        'energized': ['movement', 'journaling', 'meditation'],
        'tired': ['soundscape', 'breathing', 'meditation'],
        'happy': ['movement', 'journaling', 'visualization'],
    }

    def get(self, request):
        from apps.mood.models import MoodLog
        from datetime import timedelta

        # Get latest mood log
        latest_mood = MoodLog.objects.filter(user=request.user).order_by('-created_at').first()
        mood_score = latest_mood.score if latest_mood else 3
        emotion_tags = latest_mood.emotion_tags if latest_mood else []

        # Determine best categories
        score_categories = self.MOOD_PRACTICE_MAP.get(mood_score, ['meditation', 'breathing'])
        emotion_categories = []
        for emotion in emotion_tags:
            emotion_categories.extend(self.EMOTION_PRACTICE_MAP.get(emotion, []))

        all_categories = list(dict.fromkeys(score_categories + emotion_categories))[:4]

        # Fetch practices
        practices = MindfulnessPractice.objects.filter(
            category__in=all_categories,
            is_active=True
        ).order_by('difficulty')[:6]

        # Build recommendations with reasons
        recommendations = []
        for practice in practices:
            reason = self._generate_reason(practice, mood_score, emotion_tags)
            rec, _ = UserRecommendation.objects.get_or_create(
                user=request.user,
                practice=practice,
                created_at__date=timezone.now().date(),
                defaults={'reason': reason, 'mood_score_at_time': mood_score}
            )
            recommendations.append(RecommendationSerializer(rec).data)

        return Response({
            'mood_score': mood_score,
            'emotion_tags': emotion_tags,
            'recommendations': recommendations,
        })

    def _generate_reason(self, practice, score, emotions):
        emotion_str = ', '.join(emotions) if emotions else 'your current state'
        if score <= 2:
            return f"This {practice.category} practice can help you find stability when feeling {emotion_str}."
        elif score == 3:
            return f"A {practice.duration_minutes}-minute {practice.category} to gently lift your mood."
        else:
            return f"Build on your positive energy with this {practice.category} session."


class CompleteRecommendationView(APIView):
    """PUT /api/v1/recommendations/<id>/complete/ - Mark as completed + rate"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            rec = UserRecommendation.objects.get(id=pk, user=request.user)
            rec.is_completed = True
            rec.completed_at = timezone.now()
            rec.rating = request.data.get('rating')
            rec.save()
            return Response({'message': 'Practice completed! Great work on your wellness journey.'})
        except UserRecommendation.DoesNotExist:
            return Response({'error': 'Recommendation not found.'}, status=status.HTTP_404_NOT_FOUND)


class PracticeLibraryView(generics.ListAPIView):
    """GET /api/v1/recommendations/library/ - Browse all practices"""
    serializer_class = PracticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MindfulnessPractice.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset
