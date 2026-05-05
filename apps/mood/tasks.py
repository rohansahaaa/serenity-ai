"""Mood async tasks powered by OpenAI via Celery"""
#from celery import shared_task
import openai
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)



def analyze_mood_with_ai(self, mood_log_id):
    """
    Async task: Analyze a mood log entry using OpenAI GPT-4.
    Extracts sentiment, emotional triggers, and generates a supportive summary.
    """
    try:
        from .models import MoodLog
        mood_log = MoodLog.objects.get(id=mood_log_id)

        if mood_log.ai_processed:
            return

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = f"""
        Analyze this mood check-in and provide structured emotional support insights.
        
        Mood Score: {mood_log.score}/5
        Emotion Tags: {', '.join(mood_log.emotion_tags)}
        User Note: {mood_log.note or 'No note provided'}
        Energy Level: {mood_log.energy_level}/5
        Sleep Hours: {mood_log.sleep_hours or 'Not provided'}
        
        Respond ONLY with a JSON object with these fields:
        - sentiment: "positive", "negative", or "neutral"
        - summary: A warm, empathetic 1-2 sentence summary (50 words max)
        - triggers: A list of up to 3 potential emotional triggers identified
        """

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a compassionate mental wellness AI. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        result = json.loads(response.choices[0].message.content)

        mood_log.ai_sentiment = result.get('sentiment', 'neutral')
        mood_log.ai_summary = result.get('summary', '')
        mood_log.ai_triggers = result.get('triggers', [])
        mood_log.ai_processed = True
        mood_log.save()

        logger.info(f"AI analysis complete for MoodLog {mood_log_id}")

    except MoodLog.DoesNotExist:
        logger.error(f"MoodLog {mood_log_id} not found")
    except Exception as exc:
        logger.error(f"AI analysis failed for MoodLog {mood_log_id}: {exc}")
        raise self.retry(exc=exc, countdown=60)


#@shared_task(bind=True, max_retries=3)
def analyze_mood_with_ai(mood_log_id):
    """
    Async task: Perform NLP analysis on journal entry.
    Extracts themes, sentiment score, and key emotions.
    """
    try:
        from .models import JournalEntry
        entry = JournalEntry.objects.get(id=journal_id)

        if entry.ai_processed:
            return

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = f"""
        Perform emotional NLP analysis on this journal entry.
        
        Entry: {entry.content[:1000]}
        
        Respond ONLY with JSON:
        - themes: list of up to 5 key themes
        - sentiment_score: float from -1.0 (very negative) to 1.0 (very positive)
        - key_emotions: list of up to 4 primary emotions expressed
        """

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an empathetic NLP analyzer. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5,
        )

        result = json.loads(response.choices[0].message.content)

        entry.ai_themes = result.get('themes', [])
        entry.ai_sentiment_score = result.get('sentiment_score', 0.0)
        entry.ai_key_emotions = result.get('key_emotions', [])
        entry.ai_processed = True
        entry.save()

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


#@shared_task
def send_daily_mood_reminder():
    """Celery Beat task: Send daily mood check-in reminders at 9 AM"""
    from apps.users.models import CustomUser
    from django.utils import timezone

    users = CustomUser.objects.filter(
        is_active=True,
        notification_enabled=True,
        preferences__reminder_time__isnull=False
    )
    count = 0
    for user in users:
        # In production: send push notification / email
        logger.info(f"Sending reminder to {user.email}")
        count += 1
    return f"Reminders sent to {count} users"


#@shared_task
def generate_weekly_insights():
    """Celery Beat task: Generate weekly AI insights for all active users"""
    from apps.users.models import CustomUser
    from .models import MoodLog, MoodInsight
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Avg
    from collections import Counter

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    users = CustomUser.objects.filter(is_active=True)
    for user in users:
        logs = MoodLog.objects.filter(user=user, created_at__date__range=[start_date, end_date])
        if logs.count() < 3:
            continue

        avg_score = logs.aggregate(Avg('score'))['score__avg']
        all_emotions = []
        for log in logs:
            all_emotions.extend(log.emotion_tags)

        top_emotions = [e for e, _ in Counter(all_emotions).most_common(3)]

        MoodInsight.objects.create(
            user=user,
            period='weekly',
            start_date=start_date,
            end_date=end_date,
            average_score=round(avg_score, 2),
            dominant_emotions=top_emotions,
            improvement_areas=['sleep', 'exercise'] if avg_score < 3 else ['consistency'],
            ai_summary=f"You logged {logs.count()} mood entries this week with an average score of {avg_score:.1f}/5.",
            streak_days=logs.values('created_at__date').distinct().count(),
        )
    logger.info("Weekly insights generated")
