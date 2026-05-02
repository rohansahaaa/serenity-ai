"""AI Chat views - powered by OpenAI with Redis session caching"""
import openai
import json 
from rest_framework.response import Response
from rest_framework.decorators import api_view

from services.ai_service import AIService
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import ChatSession, ChatMessage 

@api_view(['POST'])
def mood_analysis_view(request):
    text = request.data.get("text")

    result = AIService.analyze_mood(text)

    return Response({
        "mood_response": result
    })


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'role', 'content', 'created_at')


class ChatSessionSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'is_active', 'message_count', 'created_at', 'updated_at')

    def get_message_count(self, obj):
        return obj.messages.count()


class ChatMessageView(APIView):
    """POST /api/v1/chat/message/ - Send message to AI support assistant"""
    permission_classes = [IsAuthenticated]

    SYSTEM_PROMPT = """You are Serenity, a compassionate AI mental wellness companion. 
    Your role is to provide empathetic emotional support, active listening, and gentle guidance.
    
    Guidelines:
    - Always validate the user's feelings before offering advice
    - Use trauma-informed, non-judgmental language
    - Recommend professional help when appropriate (severe distress, crisis situations)
    - Suggest evidence-based mindfulness techniques when helpful
    - Keep responses warm, concise, and supportive (100-150 words)
    - Never diagnose or prescribe; you are a supportive companion, not a therapist
    - If the user expresses crisis or self-harm, immediately provide crisis resources
    """

    def post(self, request):
        message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id')

        if not message:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=request.user)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user)

        # Load conversation history from Redis cache (fast access)
        cache_key = f"chat_history_{session.id}"
        history = cache.get(cache_key, [])

        # Save user message to DB
        ChatMessage.objects.create(session=session, role='user', content=message)
        history.append({"role": "user", "content": message})

        # Keep history window to last 20 messages to manage token usage
        if len(history) > 20:
            history = history[-20:]

        # Get recent mood context for personalized responses
        mood_context = self._get_mood_context(request.user)

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            system_with_context = self.SYSTEM_PROMPT
            if mood_context:
                system_with_context += f"\n\nUser's recent mood context: {mood_context}"

            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_with_context},
                    *history
                ],
                max_tokens=300,
                temperature=0.8,
            )

            ai_reply = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            # Save AI response
            ChatMessage.objects.create(
                session=session, role='assistant',
                content=ai_reply, tokens_used=tokens_used
            )

            # Update cache
            history.append({"role": "assistant", "content": ai_reply})
            cache.set(cache_key, history, timeout=3600)  # 1 hour TTL

            # Auto-generate session title from first message
            if session.messages.count() == 2:
                session.title = message[:60] + ('...' if len(message) > 60 else '')
                session.save()

            return Response({
                'session_id': session.id,
                'message': ai_reply,
                'tokens_used': tokens_used,
            })

        except openai.APIError as e:
            return Response({'error': 'AI service temporarily unavailable. Please try again.'},
                          status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def _get_mood_context(self, user):
        """Fetch recent mood data to personalize AI responses"""
        from apps.mood.models import MoodLog
        from django.utils import timezone
        from datetime import timedelta

        recent = MoodLog.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=3)
        ).order_by('-created_at')[:3]

        if not recent:
            return None

        avg_score = sum(l.score for l in recent) / len(recent)
        emotions = [tag for log in recent for tag in log.emotion_tags]
        return f"Average mood score: {avg_score:.1f}/5. Recent emotions: {', '.join(set(emotions))}"


class ChatSessionListView(generics.ListAPIView):
    """GET /api/v1/chat/sessions/ - List user's chat sessions"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class ChatHistoryView(generics.ListAPIView):
    """GET /api/v1/chat/sessions/<id>/history/ - Get messages in a session"""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            session__id=self.kwargs['session_id'],
            session__user=self.request.user
        )
