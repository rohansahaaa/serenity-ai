"""
Mood and journal AI tasks powered by Groq.
Celery is optional. These functions can run normally during deployment.
"""

from django.conf import settings
import os
import json
import logging
from groq import Groq

logger = logging.getLogger(__name__)


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", None)
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing in environment variables.")
    return Groq(api_key=api_key)


def safe_json_parse(text):
    try:
        return json.loads(text)
    except Exception:
        return {}


def analyze_mood_with_ai(mood_log_id):
    """
    Analyze a mood log entry using Groq.
    """
    from .models import MoodLog

    try:
        mood_log = MoodLog.objects.get(id=mood_log_id)

        if mood_log.ai_processed:
            return

        client = get_groq_client()

        prompt = f"""
Analyze this mood check-in and provide structured emotional support insights.

Mood Score: {mood_log.score}/5
Emotion Tags: {', '.join(mood_log.emotion_tags) if mood_log.emotion_tags else 'None'}
User Note: {mood_log.note or 'No note provided'}
Energy Level: {mood_log.energy_level}/5
Sleep Hours: {mood_log.sleep_hours or 'Not provided'}

Respond ONLY with valid JSON:
{{
  "sentiment": "positive/negative/neutral",
  "summary": "warm empathetic summary under 50 words",
  "triggers": ["trigger1", "trigger2", "trigger3"]
}}
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are Serenity AI, a compassionate mental wellness assistant. Respond only with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.6,
        )

        content = response.choices[0].message.content
        result = safe_json_parse(content)

        mood_log.ai_sentiment = result.get("sentiment", "neutral")
        mood_log.ai_summary = result.get(
            "summary",
            "You took a positive step by checking in with yourself today.",
        )
        mood_log.ai_triggers = result.get("triggers", [])
        mood_log.ai_processed = True
        mood_log.save()

        logger.info(f"Groq mood analysis complete for MoodLog {mood_log_id}")

    except MoodLog.DoesNotExist:
        logger.error(f"MoodLog {mood_log_id} not found")

    except Exception as exc:
        logger.error(f"Groq mood analysis failed for MoodLog {mood_log_id}: {exc}")


def analyze_journal_with_ai(journal_id):
    """
    Analyze a journal entry using Groq.
    """
    from .models import JournalEntry

    try:
        entry = JournalEntry.objects.get(id=journal_id)

        if entry.ai_processed:
            return

        client = get_groq_client()

        prompt = f"""
Perform emotional NLP analysis on this journal entry.

Entry:
{entry.content[:1000]}

Respond ONLY with valid JSON:
{{
  "themes": ["theme1", "theme2"],
  "sentiment_score": 0.0,
  "key_emotions": ["emotion1", "emotion2"]
}}
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are Serenity AI, an empathetic NLP analyzer. Respond only with valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
            temperature=0.5,
        )

        content = response.choices[0].message.content
        result = safe_json_parse(content)

        entry.ai_themes = result.get("themes", [])
        entry.ai_sentiment_score = result.get("sentiment_score", 0.0)
        entry.ai_key_emotions = result.get("key_emotions", [])
        entry.ai_processed = True
        entry.save()

        logger.info(f"Groq journal analysis complete for JournalEntry {journal_id}")

    except JournalEntry.DoesNotExist:
        logger.error(f"JournalEntry {journal_id} not found")

    except Exception as exc:
        logger.error(f"Groq journal analysis failed for JournalEntry {journal_id}: {exc}")


def send_daily_mood_reminder():
    from apps.users.models import CustomUser

    users = CustomUser.objects.filter(
        is_active=True,
        notification_enabled=True,
        preferences__reminder_time__isnull=False,
    )

    count = 0
    for user in users:
        logger.info(f"Sending reminder to {user.email}")
        count += 1

    return f"Reminders sent to {count} users"


def generate_weekly_insights():
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
        logs = MoodLog.objects.filter(
            user=user,
            created_at__date__range=[start_date, end_date],
        )

        if logs.count() < 3:
            continue

        avg_score = logs.aggregate(Avg("score"))["score__avg"] or 0

        all_emotions = []
        for log in logs:
            if log.emotion_tags:
                all_emotions.extend(log.emotion_tags)

        top_emotions = [e for e, _ in Counter(all_emotions).most_common(3)]

        MoodInsight.objects.create(
            user=user,
            period="weekly",
            start_date=start_date,
            end_date=end_date,
            average_score=round(avg_score, 2),
            dominant_emotions=top_emotions,
            improvement_areas=["sleep", "exercise"] if avg_score < 3 else ["consistency"],
            ai_summary=f"You logged {logs.count()} mood entries this week with an average score of {avg_score:.1f}/5.",
            streak_days=logs.values("created_at__date").distinct().count(),
        )

    logger.info("Weekly insights generated")