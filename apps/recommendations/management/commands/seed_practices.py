"""Management command to seed initial mindfulness practices"""
from django.core.management.base import BaseCommand
from apps.recommendations.models import MindfulnessPractice

class Command(BaseCommand):
    help = 'Seed the database with initial mindfulness practices'

    PRACTICES = [
        {'title': '4-7-8 Breathing', 'description': 'A powerful breathing technique to reduce anxiety and promote calm.', 'category': 'breathing', 'difficulty': 'beginner', 'duration_minutes': 5, 'mood_tags': ['anxious', 'stressed', 'angry'], 'instructions': 'Inhale for 4 counts, hold 7, exhale 8. Repeat 4 times.'},
        {'title': 'Body Scan Meditation', 'description': 'A full-body awareness meditation to release tension.', 'category': 'meditation', 'difficulty': 'beginner', 'duration_minutes': 12, 'mood_tags': ['stressed', 'anxious', 'tired'], 'instructions': 'Lie down. Bring awareness from toes to head, noticing sensations.'},
        {'title': 'Loving-Kindness Meditation', 'description': 'Cultivate compassion for yourself and others.', 'category': 'meditation', 'difficulty': 'beginner', 'duration_minutes': 10, 'mood_tags': ['sad', 'angry', 'lonely'], 'instructions': 'Repeat silently: May I be happy. May I be healthy. May I be at peace.'},
        {'title': '5-4-3-2-1 Grounding', 'description': 'A sensory technique to anchor you in the present moment.', 'category': 'grounding', 'difficulty': 'beginner', 'duration_minutes': 3, 'mood_tags': ['anxious', 'overwhelmed'], 'instructions': '5 things you see, 4 touch, 3 hear, 2 smell, 1 taste.'},
        {'title': 'Gratitude Journaling', 'description': 'Write three things you are grateful for to shift perspective.', 'category': 'journaling', 'difficulty': 'beginner', 'duration_minutes': 10, 'mood_tags': ['sad', 'neutral', 'happy'], 'instructions': 'Write 3 specific things you are grateful for and why.'},
        {'title': 'Box Breathing', 'description': 'Used by Navy SEALs to reset the nervous system.', 'category': 'breathing', 'difficulty': 'beginner', 'duration_minutes': 5, 'mood_tags': ['stressed', 'anxious'], 'instructions': 'Inhale 4, hold 4, exhale 4, hold 4. Repeat 8 cycles.'},
        {'title': 'Mindful Walking', 'description': 'Transform a simple walk into a meditative experience.', 'category': 'movement', 'difficulty': 'beginner', 'duration_minutes': 20, 'mood_tags': ['energized', 'restless'], 'instructions': 'Walk slowly, notice each step, sounds, sensations.'},
        {'title': 'Safe Place Visualization', 'description': 'Mentally create a peaceful sanctuary.', 'category': 'visualization', 'difficulty': 'intermediate', 'duration_minutes': 15, 'mood_tags': ['anxious', 'sad'], 'instructions': 'Close eyes. Imagine a completely safe, peaceful place. Engage all senses.'},
        {'title': 'Rain Soundscape', 'description': 'Immersive nature sounds to calm the nervous system.', 'category': 'soundscape', 'difficulty': 'beginner', 'duration_minutes': 20, 'mood_tags': ['anxious', 'stressed'], 'instructions': 'Use headphones, close eyes, breathe slowly with the sounds.'},
        {'title': 'Progressive Muscle Relaxation', 'description': 'Tense and release muscle groups to dissolve stress.', 'category': 'movement', 'difficulty': 'beginner', 'duration_minutes': 15, 'mood_tags': ['stressed', 'anxious'], 'instructions': 'Tense each muscle group 5 seconds, release 30 seconds. Work from feet to face.'},
    ]

    def handle(self, *args, **options):
        created = 0
        for data in self.PRACTICES:
            _, was_created = MindfulnessPractice.objects.get_or_create(title=data['title'], defaults=data)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} practices successfully'))
