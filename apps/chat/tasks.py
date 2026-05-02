"""Chat async tasks"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_sessions():
    """Remove chat cache entries for inactive sessions older than 30 days"""
    from .models import ChatSession
    from django.core.cache import cache

    old_sessions = ChatSession.objects.filter(
        updated_at__lt=timezone.now() - timedelta(days=30),
        is_active=True
    )
    count = 0
    for session in old_sessions:
        cache.delete(f"chat_history_{session.id}")
        session.is_active = False
        session.save()
        count += 1

    logger.info(f"Cleaned up {count} old chat sessions")
    return f"Cleaned {count} sessions"
