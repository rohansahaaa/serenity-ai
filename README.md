# Serenity AI — Smart Mental Wellness Platform

## Project Overview
Serenity AI is a Django-based mental wellness platform that analyzes mood trends and provides AI-driven emotional support using OpenAI GPT-4. It recommends personalized meditation and mindfulness practices based on the user's emotional state.

## Team Members
- (Add your team members here)

## Project Title
Serenity AI — AI-Powered Mental Wellness Platform

## Tech Stack
- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL
- **AI/NLP:** OpenAI GPT-4 API
- **Async Queue:** Celery + Redis
- **Auth:** JWT (SimpleJWT)
- **Cache:** Redis (django-redis)

## Project Structure
```
serenity_ai/
├── serenity_project/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── apps/
│   ├── users/                 # Auth, profiles, preferences
│   ├── mood/                  # Mood logging, journaling, trends
│   ├── chat/                  # AI emotional support chat
│   └── recommendations/       # Mindfulness practice recommendations
├── requirements.txt
├── manage.py
└── .env.example
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register/ | Register new user |
| POST | /api/v1/auth/token/ | Login (get JWT) |
| GET/PUT | /api/v1/auth/profile/ | User profile |
| PUT | /api/v1/auth/preferences/ | Update preferences |
| POST | /api/v1/mood/log/ | Log a mood check-in |
| GET | /api/v1/mood/logs/ | Mood history |
| GET | /api/v1/mood/trends/ | Mood trends & analytics |
| POST | /api/v1/mood/journal/ | Submit journal entry |
| GET | /api/v1/mood/insights/weekly/ | AI weekly summary |
| POST | /api/v1/chat/message/ | Chat with AI support |
| GET | /api/v1/chat/sessions/ | Chat session history |
| GET | /api/v1/recommendations/ | Personalized recommendations |
| GET | /api/v1/recommendations/library/ | All practices |
| PUT | /api/v1/recommendations/<id>/complete/ | Mark complete |

## Setup Instructions

### 1. Clone and install
```bash
git clone <repo-url>
cd serenity_ai
pip install -r requirements.txt
```

### 2. Environment variables
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Database setup
```bash
createdb serenity_db
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_practices
```

### 4. Start services
```bash
# Terminal 1 - Django server
python manage.py runserver

# Terminal 2 - Celery worker
celery -A serenity_project worker --loglevel=info

# Terminal 3 - Celery beat (scheduled tasks)
celery -A serenity_project beat --loglevel=info
```

## Key Features
1. **Mood Intelligence** — Users log mood (1-5) + emotion tags + notes. Celery triggers OpenAI analysis asynchronously.
2. **AI Support Chat** — GPT-4 powered empathetic responses. Redis caches session context for continuity.
3. **Personalized Recommendations** — Algorithm maps mood scores + emotion tags to appropriate mindfulness practices.
4. **Trend Analytics** — Streak tracking, weekly averages, dominant emotion detection.
5. **Journal NLP** — Free-form journal entries analyzed for themes, sentiment score (-1 to 1), and key emotions.
6. **Scheduled Tasks** — Celery Beat sends daily reminders and generates weekly insights automatically.

## Domain
AI / Web — Mental Health Tech
