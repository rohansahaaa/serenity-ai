import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class AIService:

    @staticmethod
    def analyze_mood(text, mood=""):
        try:
            prompt = f"""
You are Serenity AI, a calm and supportive mental wellness assistant.

User mood: {mood}
User note: {text}

Write one clean paragraph only.
The paragraph should acknowledge the user's mood, give supportive guidance,
and suggest one small practical step.

Rules:
- Use normal spacing.
- Do not use bullet points.
- Do not use markdown.
- Do not give medical advice.
- Keep it around 80 to 120 words.
"""

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a supportive wellness assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"AI temporarily unavailable. Try taking one slow breath and focus on one small step. Error: {e}"