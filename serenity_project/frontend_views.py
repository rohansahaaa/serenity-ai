from datetime import timedelta
from collections import Counter

from django.shortcuts import render
from django.utils import timezone

from apps.mood.models import MoodLog, JournalEntry
from apps.chat.ai_service import AIService




def home(request):
    return render(request, "index.html")


def dashboard(request):
    mood = request.session.get("last_mood", "Neutral")
    note = request.session.get("last_note", "")

    score = None
    summary = None
    suggestions = []

    if request.method == "POST":
        sleep = int(request.POST.get("sleep", 3))
        stress = int(request.POST.get("stress", 3))
        energy = int(request.POST.get("energy", 3))
        social = int(request.POST.get("social", 3))

        score = 50
        score += sleep * 6
        score += energy * 6
        score += social * 4
        score -= stress * 7

        if mood in ["Happy", "Calm", "Energetic"]:
            score += 10
        elif mood in ["Sad", "Anxious", "Stressed", "Tired"]:
            score -= 10

        score = max(0, min(100, score))

        if score >= 80:
            summary = "Your wellness score looks strong today. You seem emotionally stable and positive."
            suggestions = [
                "Use this good state to complete something meaningful.",
                "Share your positive energy with someone.",
                "Journal what helped you feel this way so you can repeat it.",
            ]
        elif score >= 60:
            summary = "Your wellness score is balanced. Small care habits can help."
            suggestions = [
                "Take a 5-minute breathing break.",
                "Write down one thing that went well today.",
                "Focus on one task instead of everything at once.",
            ]
        elif score >= 40:
            summary = "Your wellness score suggests mild emotional pressure."
            suggestions = [
                "Try the 4-4-6 breathing method.",
                "Break your work into smaller steps.",
                "Write what is bothering you in your journal.",
            ]
        else:
            summary = "Your wellness score is low today. Take things gently."
            suggestions = [
                "Pause and take slow breaths.",
                "Reach out to someone you trust.",
                "Do one calming activity.",
            ]

    return render(request, "dashboard.html", {
        "mood": mood,
        "note": note,
        "score": score,
        "summary": summary,
        "suggestions": suggestions,
    })


def mood_page(request):
    response = None

    if request.method == "POST":
        mood = request.POST.get("mood", "")
        note = request.POST.get("note", "")

        request.session["last_mood"] = mood
        request.session["last_note"] = note

        response = AIService.analyze_mood(note, mood)

        MoodLog.objects.create(
            mood=mood,
            note=note,
            ai_response=response
        )

    return render(request, "mood.html", {
        "response": response
    })


def chat_page(request):
    reply = None

    if request.method == "POST":
        message = request.POST.get("message", "")

        if AIService:
            reply = AIService.analyze_mood(message)
        else:
            reply = "I am here with you. Take things one step at a time."

    return render(request, "chat.html", {"reply": reply})


def recommendations_page(request):
    return render(request, "recommendations.html", {
        "practices": []
    })


def practices_page(request):
    return render(request, "practices.html")


def journal_page(request):
    saved = False

    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")

        JournalEntry.objects.create(
            title=title,
            content=content
        )

        saved = True

    journals = JournalEntry.objects.order_by("-created_at")

    return render(request, "journal.html", {
        "saved": saved,
        "journals": journals
    })


def mood_history_page(request):
    today = timezone.now()

    week_start = today - timedelta(days=7)
    month_start = today - timedelta(days=30)
    year_start = today - timedelta(days=365)

    weekly_moods = MoodLog.objects.filter(created_at__gte=week_start)
    monthly_moods = MoodLog.objects.filter(created_at__gte=month_start)
    yearly_moods = MoodLog.objects.filter(created_at__gte=year_start)

    recent_moods = MoodLog.objects.all().order_by("-created_at")[:10]

    mood_names = [m.mood for m in weekly_moods]
    common_mood = "No data"

    if mood_names:
        common_mood = Counter(mood_names).most_common(1)[0][0]

    analysis = "Start logging moods to generate analysis."

    if common_mood == "Happy":
        analysis = "Your recent mood trend is positive. Continue habits that support your happiness."
    elif common_mood == "Calm":
        analysis = "Your recent mood trend shows emotional balance and stability."
    elif common_mood == "Sad":
        analysis = "Your recent mood trend shows lower emotional energy. Journaling and rest may help."
    elif common_mood == "Anxious":
        analysis = "Your recent mood trend shows anxiety. Grounding and breathing practices may help."
    elif common_mood == "Stressed":
        analysis = "Your recent mood trend shows stress. Try breaking work into smaller tasks."
    elif common_mood == "Tired":
        analysis = "Your recent mood trend shows tiredness. Focus on rest, hydration, and light routines."

    weekly_data = []
    moods = ['Happy', 'Calm', 'Sad', 'Anxious']

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = MoodLog.objects.filter(created_at__date=day.date()).count()
        weekly_data.append({
            "label": day.strftime("%a"),
            "count": count
        })

    max_count = max([d["count"] for d in weekly_data]) if weekly_data else 1
    if max_count == 0:
        max_count = 1

    graph_points = []
    svg_width = 700
    svg_height = 260
    gap = svg_width / 6

    for index, item in enumerate(weekly_data):
        x = index * gap
        y = svg_height - ((item["count"] / max_count) * 200) - 30
        graph_points.append(f"{x},{y}")

    graph_points_string = " ".join(graph_points)

    mood_counts = Counter([m.mood for m in yearly_moods])
    total = sum(mood_counts.values()) or 1

    mood_graph = []
    for mood, count in mood_counts.items():
        mood_graph.append({
            "mood": mood,
            "count": count,
            "percent": int((count / total) * 100)
        })

    return render(request, "mood_history.html", {
        "weekly_count": weekly_moods.count(),
        "monthly_count": monthly_moods.count(),
        "yearly_count": yearly_moods.count(),
        "common_mood": common_mood,
        "analysis": analysis,
        "recent_moods": recent_moods,
        "weekly_data": weekly_data,
        "graph_points": graph_points_string,
        "mood_graph": mood_graph,
        "mood_counts": dict(mood_counts),
    })