import os
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

def send_email_alert(description, tracking_id):
    print("INSIDE EMAIL FUNCTION")
    print("EMAIL:", sender_email)
    print("PASS:", sender_password)
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    subject = "🚨 High Severity Ragging Complaint"
    body = f"""
    A high severity complaint has been reported.

    Tracking ID: {tracking_id}
    Description: {description}
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

    # 🧠 classification (your existing logic)
    category, severity = analyze_text_basic(description)

    # 🚨 flag system
    is_flagged = True if severity == "high" else False

    # ❤️ emotional support
    emotion_message = emotional_response(description)

    tracking_id = generate_tracking_id()

    if severity == "high":
        try:
            send_email_alert(description, tracking_id)
        except Exception as e:
            print("Email failed:", e)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (tracking_id, description, ai_category, ai_severity)
        VALUES (%s, %s, %s, %s)
    """, (tracking_id, description, category, severity))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Complaint submitted",
        "tracking_id": tracking_id,
        "category": category,
        "severity": severity,
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


def emotional_response(text):
    text = text.lower()

    if any(word in text for word in ["scared", "afraid", "fear", "threat"]):
        return "You are not alone. Your safety is important. Help is available."

    if any(word in text for word in ["embarrassed", "ashamed", "humiliated"]):
        return "It's okay to speak up. You did the right thing by reporting this."

    if any(word in text for word in ["bullied", "harassed", "abused"]):
        return "This behavior is not acceptable. We take this seriously and will act on it."

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

