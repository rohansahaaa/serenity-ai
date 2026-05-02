from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIService:

    @staticmethod
    def analyze_mood(text):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a calm, supportive mental wellness assistant."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception:
            return "I'm here with you. Take a slow breath. You're safe."