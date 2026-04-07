import os
from ai import analyze_with_ai
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Anti-Ragging AI Backend Running"}


from pydantic import BaseModel
from database import get_connection
import uuid
import smtplib
from email.mime.text import MIMEText

def send_email_alert(description, tracking_id, accused_name=None):
    print("INSIDE EMAIL FUNCTION")
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    subject = "🚨 High Severity Ragging Complaint"
    body = f"""
    A high severity complaint has been reported.

    Tracking ID: {tracking_id}
    Description: {description}
    Accused: {accused_name if accused_name else "Not mentioned"}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email error:", e)


# ✅ This fixes Swagger UI input
class Complaint(BaseModel):
    description: str


def generate_tracking_id():
    return str(uuid.uuid4())[:8]


@app.post("/report")
def report_complaint(data: Complaint):
    description = data.description

    # 🧠 AI ANALYSIS (Gemini)
    ai_result = analyze_with_ai(description)

    category = ai_result["category"]
    severity = ai_result["severity"]
    emotion = ai_result["emotion"]
    confidence = ai_result["confidence"]

    accused_name = ai_result.get("accused_name")
    if accused_name:
        accused_name = accused_name.strip().title()

    # 🔁 fallback
    if not accused_name:
        accused_name = extract_name_fallback(description)

    # 🚨 flag system
    is_flagged = True if severity == "high" else False

    # ❤️ emotional support
    emotion_message = emotional_response(emotion, description)

    tracking_id = generate_tracking_id()

    # 🚨 email alert
    if severity == "high":
        try:
            send_email_alert(description, tracking_id, accused_name)
        except Exception as e:
            print("Email failed:", e)

    # 💾 DB save
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints 
    (tracking_id, description, ai_category, ai_severity, emotion, confidence, accused_name)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (tracking_id, description, category, severity, emotion, confidence, accused_name))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Complaint submitted",
        "tracking_id": tracking_id,
        "category": category,
        "severity": severity,
        "emotion": emotion,
        "confidence": confidence,
        "flagged": is_flagged,
        "support_message": emotion_message
    }

@app.get("/status/{tracking_id}")
def check_status(tracking_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, description, created_at
        FROM complaints
        WHERE tracking_id = %s
    """, (tracking_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return {"error": "Tracking ID not found"}

    return {
        "tracking_id": tracking_id,
        "status": result[0],
        "description": result[1],
        "created_at": result[2]
    }

def analyze_text_basic(text):
    text = text.lower()

    # 🔴 High severity (harassment / physical abuse)
    high_keywords = ["slap", "hit", "abuse", "force", "threat"]

    # 🟡 Medium severity (ragging / bullying)
    medium_keywords = ["bully", "harass", "insult"]

    # 🔴 Check high severity
    for word in high_keywords:
        if word in text:
            return "harassment", "high"

    # 🟡 Check medium severity
    for word in medium_keywords:
        if word in text:
            return "ragging", "medium"

    # 🟢 Default
    return "ragging", "low"

@app.get("/admin/flagged")
def get_flagged_complaints():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tracking_id, description, ai_category, ai_severity, created_at
        FROM complaints
        WHERE ai_severity = 'high'
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    complaints = []

    for row in results:
        complaints.append({
            "tracking_id": row[0],
            "description": row[1],
            "category": row[2],
            "severity": row[3],
            "created_at": row[4]
        })

    return {"flagged_complaints": complaints}


def emotional_response(emotion, text=None):
    emotion = emotion.strip().lower()  # 🔥 FIX

    if emotion == "fear":
        return "You are not alone. Your safety is important. Help is available."

    elif emotion == "anger":
        return "It's okay to feel angry. Stay calm and report safely."

    elif emotion == "neutral":
        return "Thank you for reporting. We are here to support you."

    # fallback (your old logic)
    if text:
        text = text.lower()

        if any(word in text for word in ["scared", "afraid", "fear", "threat"]):
            return "You are not alone. Your safety is important. Help is available."

    return "Thank you for reporting. We are here to support you."

@app.get("/rights")
def get_rights():
    return {
        "what_is_ragging": "Any act that causes physical or mental harm, fear, embarrassment, or harassment to a student.",
        
        "examples": [
            "Forcing juniors to perform embarrassing acts",
            "Physical abuse like hitting or slapping",
            "Verbal abuse or insults",
            "Threatening or intimidating behavior"
        ],

        "punishments": [
            "Suspension from college",
            "Expulsion",
            "Fine or legal action",
            "Police complaint"
        ],

        "student_rights": [
            "Right to a safe environment",
            "Right to report anonymously",
            "Right to protection from retaliation",
            "Right to counseling and support"
        ],

        "help": "Contact Anti-Ragging Committee or use this platform to report safely."
    }


@app.get("/evidence-help")
def evidence_help():
    return {
        "title": "How to Collect Evidence Safely",

        "steps": [
            "Take screenshots of chats or messages",
            "Save date and time of incidents",
            "Record audio/video if safe",
            "Keep copies of any threats or messages",
            "Note names of people involved",
            "Identify witnesses if possible"
        ],

        "important_notes": [
            "Do not put yourself in danger while collecting evidence",
            "Keep evidence private and secure",
            "Do not share publicly on social media",
            "Submit evidence only to authorities"
        ],

        "file_types_supported": [
            "Screenshots (PNG, JPG)",
            "Videos (MP4)",
            "Audio recordings",
            "Chat logs"
        ]
    }

import re

def extract_name_fallback(text):
    words = text.lower().split()

    # 🔥 Priority: word after "by"
    if "by" in words:
        idx = words.index("by")
        if idx + 1 < len(words):
            return words[idx + 1].strip(",.!?").title()

    # 🔁 fallback: find probable name
    ignore = {"i", "me", "my", "got", "slapped", "hit", "by", "the", "a", "an", "senior"}

    for word in words:
        clean = word.strip(",.!?")

        if clean not in ignore and clean.isalpha() and len(clean) > 3:
            return clean.title()

    return None
