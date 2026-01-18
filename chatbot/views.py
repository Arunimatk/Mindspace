import json
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

from .models import Mood

import os

# Function to load .env file manually since python-dotenv is not installed
def load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_file()

# Replace with your key (or set via env and read here)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Helpers ----------
def detect_emotion(message: str):
    message_low = message.lower()
    emotions = {
        "sad": ["sad", "upset", "down", "cry", "hurt", "lonely"],
        "stress": ["stress", "stressed", "pressure", "tense", "overwhelmed"],
        "anxiety": ["anxiety", "anxious", "worry", "panic", "panic attack"],
        "anger": ["angry", "mad", "rage", "irritated"],
        "depression": ["depressed", "no hope", "empty", "tired of life", "hopeless"]
    }
    for emotion, words in emotions.items():
        for w in words:
            if w in message_low:
                return emotion
    return "normal"

def check_emergency(message: str):
    danger_phrases = [
        "suicide", "kill myself", "end my life", "i want to die",
        "want to die", "hurt myself", "self harm"
    ]
    for w in danger_phrases:
        if w in message.lower():
            return True
    return False

def breathing_reply():
    return (
        "Let's try a short grounding breathing exercise:\n"
        "1) Inhale slowly for 4 seconds\n"
        "2) Hold for 4 seconds\n"
        "3) Exhale for 4 seconds\n"
        "Repeat this 3 times. Tell me how you feel after that."
    )

MOTIVATIONS = [
    "You are stronger than you think. One step at a time.",
    "Your feelings are valid. It's okay to take a break.",
    "Small steps forward are still progress.",
    "You are not alone. Sharing helps lighten the load."
]

# ---------- Views ----------
def chatbot_page(request):
    """Renders the chat UI."""
    return render(request, "chatbot/chatbot_page.html")



@csrf_exempt
def chatbot_api(request):
    """Main chat endpoint — uses simple rules + OpenAI for full replies."""
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"reply": "Invalid JSON"}, status=400)

    user_msg = data.get("message", "").strip()
    if not user_msg:
        return JsonResponse({"reply": "Please type a message."})

    # Emergency check
    if check_emergency(user_msg):
        # Urgent safety reply (non-replacement for professional help)
        reply = (
            "I'm really sorry you're feeling this way. You matter. "
            "If you are in immediate danger, please call your local emergency number right now. "
            "If you can, please reach out to a trusted person nearby. "
            "You can also call your local suicide prevention helpline — if you share your country, I can provide the number. "
            "I'm here with you."
        )
        return JsonResponse({"reply": reply})

    # Simple rules: greetings
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(g in user_msg.lower() for g in greetings):
        return JsonResponse({"reply": "Hello! 😊 I'm here to listen. What's on your mind?"})

    # Quick breathing help
    if any(x in user_msg.lower() for x in ["panic", "panicking", "anxiety", "can't breathe", "breathless"]):
        return JsonResponse({"reply": breathing_reply()})

    # Emotion-based short reply (fast)
    emotion = detect_emotion(user_msg)
    emotion_replies = {
        "sad": "I’m sorry you’re feeling sad. Would you like to share what happened? I'm here to listen.",
        "stress": "It sounds like you’re under stress. Can you tell me what part feels most overwhelming?",
        "anxiety": "That sounds anxiety-provoking. Try to take one slow breath with me. What triggered it?",
        "anger": "Feeling angry is valid. Do you want to talk about what caused it?",
        "depression": "That sounds heavy. I'm here. When did you start feeling this way?"
    }
    if emotion in emotion_replies:
        # return the caring reply first, but also let AI expand next time user continues
        return JsonResponse({"reply": emotion_replies[emotion]})

    # Fallback to OpenAI or Simulated Smart AI
    try:
        # Check if key is the placeholder
        if not OPENAI_API_KEY or "YOUR_OPENAI_API_KEY" in OPENAI_API_KEY:
            raise ValueError("No API Key provided")

        system_prompt = (
            "You are MindSpace, a warm, empathetic, and professional mental health assistant. "
            "Your goal is to provide supportive, non-judgmental, and evidence-based emotional support. "
            "Keep responses concise (under 100 words) but meaningful. "
            "If a user seems to be in crisis, gently encourage professional help, but always be comforting first."
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=300,
            temperature=0.75
        )
        reply = response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI/Network Error (Using Smart Fallback):", e)
        
        # --- Smart Local AI Logic ---
        import re
        
        lower_msg = user_msg.lower()
        reply = ""

        # 1. Reflective "I feel" patterns
        match_feel = re.search(r"i feel (.*)", lower_msg)
        match_am = re.search(r"i am (.*)", lower_msg)
        
        if match_feel:
            feeling = match_feel.group(1).split('.')[0]  # take text until punctuation
            reply = f"It sounds like you're feeling {feeling}. What do you think is making you feel this way?"
        
        elif match_am:
            state = match_am.group(1).split('.')[0]
            reply = f"I hear you saying that you are {state}. How long have you been feeling {state}?"

        # 2. Topic-based responses
        elif "lonely" in lower_msg or "alone" in lower_msg:
            reply = "Loneliness is a heavy feeling, but you are not truly alone. Connecting with yourself or reaching out to a friend can be a small first step."
        elif "sleep" in lower_msg or "tired" in lower_msg or "insomnia" in lower_msg:
            reply = "Sleep affects everything. Have you tried a calming routine before bed, like reading or deep breathing?"
        elif "job" in lower_msg or "work" in lower_msg or "boss" in lower_msg:
            reply = "Work challenges can drain us mentally. Remember that your worth is not defined by your productivity."
        elif "family" in lower_msg or "parent" in lower_msg or "fight" in lower_msg:
            reply = "Family dynamics can be complicated. It's okay to set boundaries to protect your peace."
        elif "future" in lower_msg or "scared" in lower_msg:
            reply = "The future can be scary, but right now is where you have power. Let's focus on one small thing you can control today."
        
        # 4. Motivation & Positivity
        elif "motivation" in lower_msg or "motivate" in lower_msg or "inspire" in lower_msg:
            reply = random.choice(MOTIVATIONS)
        elif "happy" in lower_msg or "good" in lower_msg or "great" in lower_msg:
            reply = "I'm so glad to hear that! nurturing these positive moments is wonderful. What went well today?"

        # 5. Empathetic Generic Responses
        else:
            fallbacks = [
                "I'm listening. Please tell me more about that.",
                "That sounds meaningful. How does that make you feel?",
                "I understand. What kind of support do you need right now?",
                "Thank you for sharing that with me. I'm here for you.",
                "Can you elaborate on that? I want to understand better.",
                "It's brave of you to open up about this.",
                "Sending you positive thoughts. I'm here if you want to keep talking.",
                "You are doing a great job just by showing up for yourself today.",
                "Take your time. There is no rush to figure everything out.",
                "Your feelings are valid, and I'm here to support you through them."
            ]
            reply = random.choice(fallbacks)
            
    return JsonResponse({"reply": reply})



@csrf_exempt
def save_mood(request):
    """API to save mood tracking info."""
    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"status": "error", "msg": "Invalid JSON"}, status=400)

    user = data.get("user", "anonymous")
    mood = data.get("mood")
    note = data.get("note", "")

    if not mood:
        return JsonResponse({"status": "error", "msg": "Mood required"}, status=400)

    m = Mood.objects.create(user=user, mood=mood, note=note)
    return JsonResponse({"status": "ok", "id": m.id, "timestamp": m.timestamp.isoformat()})


def random_motivation(request):
    return JsonResponse({"reply": random.choice(MOTIVATIONS)})

