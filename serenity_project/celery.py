"""Celery Configuration for Serenity AI"""
import os
#rom celery import Celery
#from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serenity_project.settings')

app = Celery('serenity_ai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'daily-mood-reminder': {
        'task': 'apps.mood.tasks.send_daily_mood_reminder',
        'schedule': crontab(hour=9, minute=0),  # 9 AM daily
    },
    'weekly-insights': {
        'task': 'apps.mood.tasks.generate_weekly_insights',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    },
    'cleanup-old-sessions': {
        'task': 'apps.chat.tasks.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
