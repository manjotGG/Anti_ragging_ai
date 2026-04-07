import os
import json
import requests

# 🔐 Load API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"


# 🧠 MAIN AI FUNCTION
def analyze_with_ai(text):
    """
    Input: complaint text
    Output: structured JSON
    """

    prompt =f"""
You are an anti-ragging AI system.

Analyze the complaint below and extract structured information.

Complaint:
"{text}"

IMPORTANT:
- Identify if a PERSON NAME is mentioned.
- A name is usually a proper noun (e.g., Rahul, Manveer, Aman).
- If a name is clearly mentioned, return it EXACTLY.
- If no name is present, return null.

Return ONLY JSON in this format:

{{
  "category": "ragging | harassment | normal",
  "severity": "low | medium | high",
  "emotion": "fear | anger | neutral",
  "confidence": 0.0-1.0,
  "accused_name": "name or null"
}}
"""
    try:
        response = requests.post(
            GEMINI_URL,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }
        )

        result = response.json()

        # 🧠 Extract text response
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]

        # 🧹 Clean JSON (sometimes Gemini adds extra text)
        cleaned = raw_text.strip().replace("```json", "").replace("```", "")

        return json.loads(cleaned)

    except Exception as e:
        print("AI Error:", e)
        return fallback_logic(text)


# 🔁 FALLBACK (VERY IMPORTANT)
def fallback_logic(text):
    text = text.lower()

    if "slap" in text or "hit" in text or "threat" in text:
        return {
            "category": "harassment",
            "severity": "high",
            "emotion": "fear",
            "confidence": 0.5
        }

    elif "fun" in text or "joke" in text:
        return {
            "category": "normal",
            "severity": "low",
            "emotion": "neutral",
            "confidence": 0.4
        }

    return {
        "category": "ragging",
        "severity": "medium",
        "emotion": "fear",
        "confidence": 0.5
    }


# 🎙️ VOICE SUPPORT (READY)
def speech_to_text(audio_file_path):
    """
    Placeholder for voice → text
    You can later integrate:
    - OpenAI Whisper
    - Google Speech API
    - Browser SpeechRecognition
    """

    # For now just simulate
    print("Voice input received:", audio_file_path)

    return "Converted speech text example"